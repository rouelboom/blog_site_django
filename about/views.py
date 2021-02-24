from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['text_in_square'] = ('<a href="https://github.com/'
                                     'rouelboom">Мой Github</a><br>'
                                     '<a href="https://t.me/vsband_pvl">'
                                     'Мой Telegram</a>')
        context['main_text'] = ('<p>Спасибо что зашли на эту страницу. '
                                'Автору приятно.</p>')
        context['header_text'] = ('Об авторе проекта')
        context['card_header_text'] = ('Контакты:')

        return context


class AboutTechView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['text_in_square'] = ('Всему виной <a href="https://'
                                     'praktikum.yandex.ru/backend-developer/">'
                                     'вот эти ребята</a>')

        context['main_text'] = ('<img src="'
                                '{% static "trolleubus.jpg" %}">')
        context['header_text'] = ('О технологиях')
        context['card_header_text'] = ('Пояснение:')
        return context
