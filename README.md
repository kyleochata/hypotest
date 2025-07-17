# hypotest
ibm hypothesis 

Leveraging customer information is important for most businesses. This project is to practice hypothesis testing to help decide, using statistical evidence, a certain effect of an attribute or a combination of attributes on insurance claims. This is to highlight the imoprtance of the inital steps of decision making before buildingteh prediction models and classifiers.

Concepts Touched:
- Understand the elements of hypothesis testing:
    - choose a sample statistic
    - Define hypothesis
    - Set the decision criteria
    - Evaluate and interpret results

Packages needed are:
- reqeusts for data fetching 
- pandas for managing data
- numpy for math operations
- seaborn for data visualization
- matplotlib for data visualization
- plotly.express for data visualization
- statsmodels for statistical analysis
- sklearn for machine learning & machine-learning pipeline related functions

## Findings
![heatmap_features]()


![price_correlation graph]()


![explained variance]()



## Set up venv
Create the virtual environment to download needed packages
```bash
    python3 -m venv venv
```
Activate environment:

MAC/Linux
``` 
 source venv/bin/activate 
```
Windows(CMD)
```
    .\venv\Scripts\activate.bat
```
Windows(PowerShell)
```
    .\venv\Scripts\Activate
```

Install packages:
```
    pip isntall pandas seaborn numpy matplotlib scikit-learn requests plotly pathlib
```

To ensure that the packages are installed run `pip list` in the terminal with the venv active

**Known issue**:
    Be sure to change the interpreter to the venv corresponding interpreter to recognize the downloaded packages