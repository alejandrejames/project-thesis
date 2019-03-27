# project-thesis

## Description
![imagesample](http://i64.tinypic.com/mkhmqw.jpg)
A topic modelling toolkit that can collect, pre-proccess, generate topic models, and visualize them through
a Graphical User Interface in Python.

## Tools/proccesses/algorithms used:
This tool uses the following tools/proccesses:
* Data Collection
  * [GetOldTweets-python by Jefferson Henrique](https://github.com/Jefferson-Henrique/GetOldTweets-python)
 * Date Pre-proccessing
  * Gensim's simple pre-proccess,
  * Spacy english model,
  * NLTK's stopwords
 * Generating Topic Models
  * Gensim's Latent Dirichlet Allocation Algorithm(LDA)
  * MALLET's Latent Dirichlet Allocation Algorithm(LDA) using the Gensim Wrapper
  * Sci-kit's Non-negative Matrix Factorization
 * Visualization
  * WordCloud
  * MatPlotLib
  * pyLDAVis(for LDA only)

## How to install
**NOTE: THIS SOFTWARE USES PYTHON 3.6.5 USING OTHER VERSIONS OF PYTHON IS NOT RECOMMENDED FOR SOME
         PACKAGES REQUIRE THE 3.6 VERSION OF PYTHON.**
**REQUIREMENTS**
1. Windows Environment
2. Python 3.6.5(path must be added through the installation)
3. Microsoft Visual C++ 2015 Redist
4. Microsoft Visual Build Tools
**INSTALLATION**
1. Download all the required packages stated below through the pip command in the command line in 
windows(e.g. pip install pandas --user). You can include the --user if you are getting an error in
the permisions.
  * pandas
  * nltk
  * gensim
  * sklearn
  * spacy
  * pprint
  * wordcloud
  * matplotlib
  * pyldavis
 2. After installing all the packages type this to the command line to download the spacy english model
 `python3 -m spacy download en`.
 3. After the download through the command line enter `python` this will show the python environment in
 the command line and input `import nltk` and then input `nltk.download('stopwords')`.
 4. After performing step 1-3 just double click the **Topic Modelling Tool.bat** inside the downloaded folder
 and it will show the command line and the GUI. **Note: Do not close the command line when opening the application
 or it will also close the application**.
 
 ## UPDATES
 **3-28-2019**
 **Added Version 1.0 of the Toolkit**
