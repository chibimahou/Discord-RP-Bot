class Character:
    def __init__(self, strength=5, speed=5, dexterity=5, fishing=0, regen=0):
        self.strength = strength
        self.speed = speed
        self.dexterity = dexterity
        self.fishing = fishing
        self.regen = regen

    def set_attributes(self, attributes):
        self.strength = attributes["strength"]
        self.speed = attributes["speed"]
        self.dexterity = attributes["dexterity"]
        self.fishing = attributes["fishing"]
        self.regen = attributes["regen"]
                
    def apply_boosts_from_string(self, input_string):
        # Define the boost-keyword and value mappings
        boosts = {
            'strength boost': 5,
            'speed boost': 3,
            'dexterity boost': 2,
            'bass pro': 3,
            "hp regen": 5
            # Add more boosts and their corresponding values as needed
        }

        # Split the input_string into individual words
        words = input_string.split(',')

        for word in words:
            word = word.strip()
            if word in boosts:
                boost_value = boosts[word]
                if word == 'bass pro':
                    attribute_name = 'fishing'
                elif word == "strength boost":
                    attribute_name = "strength"
                elif word == "defense boost":
                    attribute_name = "defense"
                elif word == "dexterity boost":
                    attribute_name = "dexterity"
                elif word == "speed boost":
                    attribute_name = "speed"
                elif word == "charisma boost":
                    attribute_name = "charisma"
                #Add more whenever adding a new boost                    
                else:
                    attribute_name = word.split()[0]
                current_value = getattr(self, attribute_name)
                setattr(self, attribute_name, current_value + boost_value)

    def get_attributes(self):
        return {
            'strength': self.strength,
            'speed': self.speed,
            'dexterity': self.dexterity,
            'fishing': self.fishing
        }

# External function that receives the input string and returns the updated character attributes
def process_boosts(input_string):
    character = Character()
    character.set_attributes({
            'strength': 9,
            'speed': 9,
            'dexterity': 9,
            'fishing': 1,
            "regen": 10
            # Add more boosts and their corresponding values as needed
        })
    character.apply_boosts_from_string(input_string)
    return character.get_attributes()

# Test the external function
input_string = "strength boost, test, value, bass pro"

updated_attributes = process_boosts(input_string)
print(updated_attributes)