INFO = {
    'baseUrl': 'https://www.comixology.eu',
    'products': {
        'Archie-2015-Vol-2/digital-comic/435686': 4,
        'Miles-Morales-Spider-Man-2018-1/digital-comic/720263': 1,
        'Spider-Gwen-Ghost-Spider-2018-1/digital-comic/703387': 1
    }
}


def get_current_value(elements):
    ''' Parse the current value from elementTree '''
    price_string = elements.xpath("//h5[@itemprop='price']/text()")[0]
    return float(price_string.replace('\xa0€','').replace(',','.'))


def get_title(elements):
    ''' Parse the title from elementTree '''
    return elements.xpath("//h1/text()")[0]


def condition(current, target):
    ''' Give the condition that needs to be met for the notification '''
    return current <= target
