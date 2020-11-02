##############################################################
#
#	RecipeParser:
#           Contains a mixin to automatically parse 
#           and run phase retrieval recipe strings.
#
#	    Siddharth Maddali
#	    Argonne National Laboratory
#	    Sep 2019
#           6xlq96aeq@relay.firefox.com
#
##############################################################

class Mixin:
    
    def generateAlgoDict( self ):
        self._algodict = { # key = string, value = function handle
            'BE':self.BinaryErosion,
            'ER':self.ER, 
            'HIO':self.HIO, 
            'SF':self.SF, 
            'SR':self.Shrinkwrap
        }
        return

    def _parseBlock( self, blockstr ):
        lst = blockstr.split( ':' )
        conv = int if len( lst )==2 else float
        self._algodict[ lst[0] ](
            *tuple( [ conv( n ) for n in lst[1:] ] )
        )
        return

    def runRecipe( self, recipestr ):
        '''
        
        runRecipe( recipestr ):

        Argument recipestr is a concatenation of smaller 'block' strings, 
        each of the form '<algo>:<iter>' and delimited by '+'. Here, 
        <algo> is the specific algorithm to be used and <iter> is the 
        number of desired iterations. For example, 'ER:30' denotes 30 
        iterations of ER. 

        For the special case of shrinkwrap, the block has the following 
        format: 'SR:<sigma>:<thresh>'. Please see Shrinkwrap documentation 
        for the meaning of sigma and thresh. 
        Algorithm keys (TODO: make case-insensitive): 
             ER: error reduction
            HIO: hybrid input/output
             SF: solvent flipping
             SR: shrinkwrap

        As an example, for a recipe of 40 iterations of ER followed by 25 HIO, 
        followed by 40 solvent flipping, with shrinkwrap (sigma=3, thresh=0.1) 
        after every 20 iterations of ER and SF, the recipe string is:

        ER:20+SR:3:0.1+ER:20+SR:3:0.1+HIO:25+SF:20+SR:3:0.1+SF:20+SR:3:0.1

        The above string is parsed and the recipe is automatically run by this 
        routine. Such recipe strings can easily be generated with Python's 
        fantastic string manipulation and list comprehension capabilities.
        
        '''
        [ 
            self._parseBlock( block ) 
            for block in recipestr.split( '+' ) 
        ];  # Don't remove this semicolon!
        return
