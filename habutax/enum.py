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

filing_status = make('1040 Filing Status', {
	'Single': "single, unmarried, or legally separated",
	'MarriedFilingJointly': "married and filing a joint return",
	'MarriedFilingSeparately': "married and file a separate return",
	'HeadOfHousehold': "unmarried and provide a home for certain other person",
	'QualifyingWidowWidower': "generally filed if your spouse died in the two years previous to the tax year of this return, you didn't remarry before the end of this tax year, and you have a child or stepchild whom you can claim as a dependent (see Form 1040 instructions for more)"
})

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
	'WY': 'Wyoming'
})

taxpayer_or_spouse = make('Taxpayer or Spouse', {
	'taxpayer': 'This belongs to the taxpayer',
	'spouse': 'This belongs to the taxpayer\'s spouse (if filing a joint return)'
})

taxpayer_spouse_or_both = make('Taxpayer, Spouse, or Both', {
	'taxpayer': 'This belongs to the taxpayer',
	'spouse': 'This belongs to the taxpayer\'s spouse (if filing a joint return)',
	'both': 'This belongs to both the taxpayer and their spouse (if filing a joint return)'
})
