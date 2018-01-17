"""
Modifiy a DataFrame

Mutators change dataframes (e.g. rename columns).  
The mutate function takes a DataFrame and returns a 
mutated copy of that DataFrame
"""
from transparency.action import Action


class Mutator(Action):
    def mutate(self, df):
        """
        call mutate, but override in_place_mutate
        """
        return self.in_place_mutate(df.copy())

    def in_place_mutate(self, df):
        """
        Override in_place_mutate.  You can modifiy the DataFrame in place, or not, as it has already been copied
        """
        raise NotImplementedError()
