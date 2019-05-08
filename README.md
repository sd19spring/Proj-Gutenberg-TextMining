# TextMining - A Project for SoftDes
This code enables a few powerful computational tools to analyze text from Project Gutenberg. These tools include comparing and plotting the similarity of two texts, as well as generating markov chains trained on any text from Project Gutenberg that can be compared in similarity to each other and to markov chains trained on another text.

# Instructions to run:
Ensure that the dependencies for this project are installed:
`pip install requirements`.
Run `automatic_text_mining.py` in the terminal. Some user input is required, but the program walks you through the steps. And that's it! All necessary files are automatically downloaded and parsed if need be, and opened if they have already been downloaded and parsed. The parameters in `automatic_text_mining.py` are adjusted for my preferred use, but they may be tweeked as desired. One important thing to note is that the program will fail if the parameter that specifies the length of the markov chain is longer than the book itself - make sure that you adjust this parameter accordingly if analyzing shorter texts.

# Features
- Automatic handling of all files from Project Gutenberg
  - The text analysis tools in this code require training text to be downloaded from Project Gutenberg. There is no need to download any files from Project Gutenberg yourself, as the program will handle this on its own. Simply type in the names of the books that you want to be analyzed, and as long as they are in Project Gutenberg, the rest will be handled for you.
- Generation of Markov chains
  - This code is able to produce markov chains from any text that is provided. There are a couple different methods for generating markov chains used:
  
  
   - - Control method: so called control because it provides a control markov chain that the rest can be compared to, this markov chain is not randomly generated and in fact just a chunk of words randomly pulled from the book.
   - - Random method: so called random because it produces your typical markov chain from randomly selected words. This marov chain is generated with a randomly chosen seed word and each consecutive word is randomly chosen from a list of words that follow that word in the book (each word having the same frequency as seen following that word in the text).
   - - Assisted method: so called assisted because it weights its choice of words depending on the ATF (augmented term frequency) of each word: This method works the same as the previous one except that the frequency of each possible word following a given word in the text is proportional to its ATF value. 
   
   
  - The code produces a sample output of each type of chain in the command line, then generates more for analysis. The sample chains are always 30 words in length, and the ones used for analysis can be of any desired length. 
- Similarity analysis of markov analyses
  - Every markov chain that is generated is fed into code that calculates the similarity matrix of the texts.
  - The similarity matrix is calculated using the cosine similarity between texts. The cosine similarity is predecated on texts being represented as vectors where each value in the vector is a number representing the word. In this case, the value used is the TF-IDF value. (If you would like to change how the TF-IDF value is weighted/found, you can go into the text and do so - no API was used to do any of the calculations). 
  - The similarity is then transformed and plotted as a scatterplot so the difference between markov chains can be seen. 
  
  - - For n markov chains generated, the first n/3 poitns (labeled with numbers) represent the control markov chain, the points n/3 -> n/2 represent the random markov chain, and the points n/2 -> n/3 points represent the assisted markov chain. For example, with the default 3 markov chains generated, points 0-1 represent the control markov, points 2-3 represent the random markov chains, and points 4-5 represent the assisted markov chains. This pattern repeats when two texts are being considered. 
