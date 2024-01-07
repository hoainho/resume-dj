import random
import string

import stripe
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View
from .forms import PaymentForm
from .models import EducationItem, Order, Payment, SkillItem, UserProfile, ProjectItem, ExperienceItem
from django.template import RequestContext
from django.core.mail import send_mail
# Email Loader
from django.template.loader import render_to_string

# and if you need to use Python's email module
stripe.api_key = settings.STRIPE_SECRET_KEY


def handler_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request, *args, **argv):
    response = render('errors/500.html', {},
                                  context_instance=RequestContext(request))
    return response

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("api:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(
                        userprofile.stripe_customer_id)
                    customer.sources.create(source=token)

                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email,
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source=token
                    )

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("/")

            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")

class IntroView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, *args, **kwargs):
        try:
            profiles = UserProfile.objects.all()
            print('user name : ', profiles.first().user.username)
            context = {
                'profiles': profiles,
            }
            return render(self.request, 'pages/introduce_page/intro.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "The user profile not found, will redirect to a default page")
            return redirect("/v1/nho/")
 
class HomeView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isOpen = False

    def get(self, *args, **kwargs):
        try:
            user_name = kwargs.get('user_name')
            if kwargs.get('user_name') == 'default':
                user_name = 'nho'
            user_profile = UserProfile.objects.get(user__username=user_name)
            context = {
                'title': 'Home',
                'profile': user_profile,
                'user': self.request.user,
                'isOpenNavbar': self.isOpen,
            }
            return render(self.request, 'home.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "The user profile not found, will redirect to a default page")
            return redirect("/v1/nho/")
        
    def openNavbar(self):
        return not self.isOpen;
    
class ResumeView(View):
    def get(self, *args, **kwargs):
        main_skills = SkillItem.objects.filter(user__username=kwargs.get('user_name'), type="K");
        sub_skills = SkillItem.objects.filter(user__username=kwargs.get('user_name'), type="O");
        experiences = ExperienceItem.objects.filter(user__username=kwargs.get('user_name'));
        educations = EducationItem.objects.filter(user__username=kwargs.get('user_name'));
        user_profile = UserProfile.objects.get(user__username=kwargs.get('user_name'))
        context = {
            'title': 'Resume',
            'profile': user_profile,
            'skills': {
                'main': main_skills,
                'sub': sub_skills
            },
            'projects': experiences,
            'educations': educations
        }
        return render(self.request, 'resume.html', context)

class ProjectView(View):
    def get(self, *args, **kwargs):
        projects = ProjectItem.objects.filter(user__username=kwargs.get('user_name'));
        user_profile = UserProfile.objects.get(user__username=kwargs.get('user_name'))
        context = {
            'title': 'Project',
            'profile': user_profile,
            'projects': projects,
        }
        return render(self.request, 'project.html', context)

class ContactView(View):
    def get(self, *args, **kwargs):
        user_profile = UserProfile.objects.get(user__username=kwargs.get('user_name'))
        context = {
            'title': 'Contact',
            'profile': user_profile,
        }
        return render(self.request, 'contact.html', context)
    def post(self, *args, **kwargs):
        user_profile = UserProfile.objects.get(user__username=kwargs.get('user_name'))
        first_name = self.request.POST.get('first-name') or ""
        last_name = self.request.POST.get('last-name') or ""
        email_address = self.request.POST.get('email') or ""
        subject = self.request.POST.get('subject') or ""
        message = self.request.POST.get('message') or ""
        msg_html = render_to_string('mail/news.html', { 'messages': message, 'subject': subject, 'full_name': first_name + " " + last_name, 'phone': user_profile.phone })
        print("Message: " + msg_html)
        context = {
            'title': 'Contact',
            'profile': user_profile,
            'default_value': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email_address,
               'subject': subject,
               'message': message,
            }
        }
        if first_name and last_name and email_address and subject and message:
            try:
                # msg = "<strong>This's message from Resume Page</strong>"
                res = send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    html_message=msg_html,
                )
                messages.success(self.request, "Your message was sent successfully" + str(res))
                return render(self.request, 'contact.html', context)
            except Exception as e:
                messages.warning(self.request, "Your message was not sent" + str(e))
                return render(self.request, 'contact.html', context)
                
        messages.warning(self.request, "Invalid data received")
        return render(self.request, 'contact.html', context)


class LogoutView(View):
    template_name = "logout.html"
