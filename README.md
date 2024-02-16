# ContaminationMadrid
This proyect has the objective of measuring the NO2 gas in Madrid in 2018 but with the vision and perspective of building a database for NO2 contamination as a wider and more up to date order. 
This is a guide to show the different scripts and functionalities.
### Data Extraction
From the links found in the pdf the data is extracted, theses links are from the Comunidad de Madrid main webpage. The future goal is to extract automatically the information from the webpage, but as an inial approach the data has to be downloaded previously and unziped. Create in the main folder another folder named DataBase and a folder for each year. Once this proccess is done simply activate the environment with the requirements.txt file and execute the following command. 
>  python .\Code\cleaningProcess.py -path ./FolderWithFilesOfYear -year year

***Example***:  

>  python .\Code\cleaningProcess.py -path ./Anio202112 -year 2021s
This will build the Database Structure and proccess and change the values of the original data so they are more readable.
### EDA Jupyter Notebook
This notebook covers just a few details of the data distribution, there are cases and examples inside.
### Future prediction
This notebook covers a future prediction of the values of NO2 contamination
### PPT presentation
This presentation shows the future of the project, how it can be implemented and the differente ways to improve the current basic one.
