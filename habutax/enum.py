from enum import Enum

# Mixin which changes the string formatting to only include the name
class StringyEnum(object):
    def __str__(self):
        return self.name

def make(name, options):
    assert(type(options) == dict)
    for k, v in options.items():
        assert(isinstance(k, str)) 
        assert(isinstance(v, str)) 
    return Enum(name, options, type=StringyEnum)

us_states = make('US States', {
	'AL': 'Alabama',
	'AK': 'Alaska',
	'AZ': 'Arizona',
	'AR': 'Arkansas',
	'CA': 'California',
	'CO': 'Colorado',
	'CT': 'Connecticut',
	'DE': 'Delaware',
	'FL': 'Florida',
	'GA': 'Georgia',
	'HI': 'Hawaii',
	'ID': 'Idaho',
	'IL': 'Illinois',
	'IN': 'Indiana',
	'IA': 'Iowa',
	'KS': 'Kansas',
	'KY': 'Kentucky',
	'LA': 'Louisiana',
	'ME': 'Maine',
	'MD': 'Maryland',
	'MA': 'Massachusetts',
	'MI': 'Michigan',
	'MN': 'Minnesota',
	'MS': 'Mississippi',
	'MO': 'Missouri',
	'MT': 'Montana',
	'NE': 'Nebraska',
	'NV': 'Nevada',
	'NH': 'New Hampshire',
	'NJ': 'New Jersey',
	'NM': 'New Mexico',
	'NY': 'New York',
	'NC': 'North Carolina',
	'ND': 'North Dakota',
	'OH': 'Ohio',
	'OK': 'Oklahoma',
	'OR': 'Oregon',
	'PA': 'Pennsylvania',
	'RI': 'Rhode Island',
	'SC': 'South Carolina',
	'SD': 'South Dakota',
	'TN': 'Tennessee',
	'TX': 'Texas',
	'UT': 'Utah',
	'VT': 'Vermont',
	'VA': 'Virginia',
	'WA': 'Washington',
	'WV': 'West Virginia',
	'WI': 'Wisconsin',
	'WY': 'Wyoming'}
)

taxpayer_or_spouse = make('Taxpayer or Spouse', {
	'taxpayer': 'This belongs to the taxpayer',
	'spouse': 'This belongs to the taxpayer\'s spouse (if filing a joint return)'
})

taxpayer_spouse_or_both = make('Taxpayer, Spouse, or Both', {
	'taxpayer': 'This belongs to the taxpayer',
	'spouse': 'This belongs to the taxpayer\'s spouse (if filing a joint return)',
	'both': 'This belongs to both the taxpayer and their spouse (if filing a joint return)'
})
