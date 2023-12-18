


def list_icons(request):
    return [{
      'label': "About me",
      'link': "/",
    },
    {
      'label': "Resume",
      'link': "/resume",
    },
    {
      'label': "Projects",
      'link': "/projects",
    },
    {
      'label': "Contact",
      'link': "/contact",
    }]

def list_footer(request):
    return [{
      'label': '<i class="fa-brands fa-facebook"></i>',
      'link': "https://www.facebook.com/beduong.nguyen.773",
    },
    {
      'label': '<i class="fa-brands fa-instagram"></i>',
      'link': "https://www.instagram.com/brduong",
    },
    {
      'label':'<i class="fa-brands fa-linkedin"></i>',
      'link': "https://www.linkedin.com/in/nguy%E1%BB%85n-th%E1%BB%8B-b%C3%A9-d%C6%B0%C6%A1ng-39242a298/",
    }]
