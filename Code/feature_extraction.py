#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 10:07:10 2018

@author: victorzhang
"""

import pandas
import os
import glob
import sys
import re
import math
def loadCSV(csvPath):
    global columnNames
    #check if the file exist
    if os.path.isfile(csvPath):
        return pandas.read_csv(csvPath)
    else:
    #if not exist, create an empty csv file
        df = pandas.DataFrame(columns = columnNames)
        return df
    
def saveCSV(outPath, df, fileName):
    if not os.path.isdir(outPath):
        os.mkdir (outPath)
    fileName = outPath + '/' + fileName
    df.to_csv(fileName, index = False)
    print ('done!')
    
def featureExtraction(df):
    quantitative = ['QUANTI_statistics', 'QUANTI_mathematics', 'QUANTI_probability', 'QUANTI_linear algebra']
    scripting = ['SCR_Python','SCR_R','SCR_Java','SCR_JavaScript','SCR_C++','SCR_C','SCR_Matlab','SCR_Pearl', 'SCR_C#']
    cs = ['CS_algorithm','CS_data structure','CS_data wrangling','CS_Data warehousing', 'CS_data mining', 'CS_VBA',
        'CS_SAS','CS_distributed computing','CS_parallel computing','CS_format conversion','CS_HTML','CS_pandas']
    database = ['DB_sql', 'DB_nosql', 'DB_access', 'DB_teradata','DB_oracle database']
    ml = ['ML_NLP', 'ML_deep learning', 'ML_machine learning', 'ML_computer vision', 'ML_tensorflow', 'ML_scikit-learn']
    software = ['SW_aws', 'SW_linux','SW_google cloud', 'SW_azure', 'SW_redshift', 'SW_git', 'SW_server','SW_api']
    bigData = ['BD_hadoop','BD_scala','BD_apache','BD_hive','BD_D3','BD_big data' ,'BD_spark']
    datavisualization = ['VISUAL_excel','VISUAL_tableau','VISUAL_ggplot','VISUAL_plotly','VISUAL_matplotlib','VISUAL_chartio','VISUAL_data visualization','VISUAL_powerpivot']
    experience = ['experience']
    domainKnowledge = ['DK_economics','DK_healthcare','DK_business','DK_finance','DK_management','DK_customer service','DK_marketing']
    communication = ['COMM_presentation','COMM_verbal','COMM_writting','COMM_interpersonal skills']
    degree = ['degree requirment']
    background = ['computer science','data science','electrical engineering','statistics', 'mathematics' ,'physics','finance','informatics']
    
    
    '''skillCategory = ['Quantitative Skills', 'Scripting Skills', 'CS Skills', 
                     'Database Skills', 'Machine Learning Skills', 'Software Skills' ,
                     'Big Data Skills', 'Data Visualization Skills', 'Prior Experience',
                     'Domain Knowledge', 'Communication Skills', 'Degree Requirement', 'Education Background']'''
    
    skillDetails = quantitative + scripting + cs + database + ml + software + bigData + datavisualization + experience + domainKnowledge + communication + degree + background

    jobInfo = ['jobID', 'jobTitle', 'positionName' ,'positionType', 'estimatedWage']
    
    localeInfo = ['jobCity', 'jobState','locationFilterUsedInSearch']
    
    compantInfo = ['rating','companySize', 'companyRevenue', 
                   'companyIndustryField', 'companyWebsite', 'companyType',
                   'companyCompetitors' , 'companyHeadQuarter', 'foundedTime']
    
    columnNames = jobInfo + localeInfo + compantInfo  + skillDetails
    answer = pandas.DataFrame(columns = columnNames)
    for row in range (len(df)):
        rowDict = df.iloc[row, :].to_dict()
        rowJobInfo = convertJobInfo(rowDict)
        rowLocaleInfo = convertLocation(rowDict['jobLocation'], rowDict ['locationFilterUsedInSearch'] ) 
        rowCompanyInfo = convertCompanyInfo(rowDict)
        #rowSkillCategory = convertCategory(rowDict)
        rowSkillSets = convertSkills(rowDict['jobDescription'])
        #print (rowSkillSets)
        row = rowJobInfo + rowLocaleInfo + rowCompanyInfo + rowSkillSets
        newDf = pandas.Series(row, index = columnNames)
        answer = answer.append(newDf, ignore_index = True)
    return answer
def convertJobInfo(rowDict):
    id = rowDict['jobID']
    title = rowDict['jobTitle']
    if re.search('analyst|analysis', title.lower()):
        position = 'Data Analyst'
    if re.search('scientist', title.lower()):
        position = 'Data Scientist'
    position = ' '.join (rowDict['keywordUsedInSearch'].split()[:-1])
    if position == 'Data Science' or position == 'Data Scientist':
        position = 'Data Scientist'
    if re.search('inter|co-op|internship', title.lower()) or re.search('inter|co-op|internship', rowDict['jobDescription'].lower()):
        positionType = 'Intern'
    else:
        positionType = 'Fulltime'
    wage = rowDict['estimatedWage']
    return [id, title, position, positionType, wage]
def convertLocation(jobLocation, filterUsed):
    myDict = {'SJ':'San Jose', 'SF': 'San Fransisco', 'LA': 'Los Angeles', 'NYC': 'New York City',
              'SD': 'San Diego', 'NewJersey': 'New Jersey', 'WashingtonDC': 'Washington D.C'}
    state = jobLocation.split('_')[-1]
    city = ' '.join (jobLocation.split('_')[:-1])
    try:
        keywordUsd = myDict[filterUsed]
    except:
        keywordUsd = filterUsed
    
    return [city, state, keywordUsd]


def convertCompanyInfo(rowDict):
    rating = rowDict['rating']
    if math.isnan(rating):
        rating = None
    size = str (rowDict['companySize'])
    if size.startswith('nan'):
        size = None
    
    revenue = str (rowDict['companyRevenue'])
    if revenue.startswith(' Unknown') or revenue.startswith('nan'):
        revenue = None
        
    field = str (rowDict['companyIndustryField'])
    if field.startswith(' Unknown') or field.startswith('nan'):
        field = None
        
    website = str(rowDict['companyWebsite'])
    if (not website.startswith('www'))  or website.startswith('nan'):
        website = None
        
    companyType = str (rowDict['companyType'] )
    if companyType.endswith('(*)'):
        index = companyType.find('(')
        companyType = companyType[:index - 1]
    if companyType.startswith('nan'):
        companyType = None 
        
    competitors = str (rowDict['companyCompetitors'])
    if competitors.startswith(' Unknow') or competitors.startswith('nan'):
        competitors = None
        
    headquarter = str (rowDict['companyHeadQuarter'])
    if headquarter.startswith('nan'):
        headquarter = None 
        
    foundedTime = str (rowDict['foundedTime'])
    if foundedTime.startswith(' Unknown') or foundedTime.startswith('nan'):
        foundedTime = None 
    
    return [rating, size, revenue, field, website, companyType, competitors, headquarter, foundedTime]
    


def convertSkills(jobDescription):
    jobDescription = jobDescription.lower()
    quantitative = getQuantitative(jobDescription)
    scripting = getScripting (jobDescription)
    cs = getCS(jobDescription)
    database = getDataBase(jobDescription)
    ml = getMachineLearnign(jobDescription)
    software = getSoftware(jobDescription)
    bigData = getBigData(jobDescription)
    datavisualization = getVisualization (jobDescription)
    experience = getExperience (jobDescription)
    domainKnowledge = getDomainKnowledge(jobDescription)
    communication = getCommunication(jobDescription)
    degree = getDegree(jobDescription)
    background = getBackground(jobDescription)
    return quantitative + scripting + cs + database + ml + software + bigData + datavisualization + experience + domainKnowledge + communication + degree + background
    
    
    
def getQuantitative(jobDescription):
    stats = math = probability = linearAlgebra = 0
    #quantitative = ['QUANTI_statistics', 'QUANTI_mathematics', 'QUANTI_probability', 'QUANTI_linear algebra']
    if re.search('statistics|stats', jobDescription):
        stats = 1
    if re.search('math|mathematics',jobDescription ):
        math = 1
    if re.search('probability', jobDescription):
        probability = 1
    if re.search('linear algebra', jobDescription):
        linearAlgebra = 1
    return [stats, math, probability, linearAlgebra]
      
def getScripting(jobDescription):
    #scripting = ['SCR_Python','SCR_R','SCR_Java','SCR_JavaScript','SCR_C++','SCR_C','SCR_Matlab','SCR_Pearl', 'SCR_C#']
    py = r = java = js = cpp = c = matlab = pearl = chashtag = 0
    if re.search('python|py', jobDescription):
        py = 1
    if re.search(' r |,r ', jobDescription):
        r = 1
    if re.search('java',jobDescription):
        java = 1
    if re.search('javascript|js', jobDescription):
        js = 1
    if re.search('cpp|c\+\+', jobDescription):
        cpp = 1
    if re.search(' c ', jobDescription):
        c = 1
    if re.search('matlab', jobDescription):
        matlab = 1
    if re.search('pearl', jobDescription):
        pearl = 1
    if re.search('c#', jobDescription):
        chashtag = 1
    return [py , r , java , js , cpp , c , matlab , pearl, chashtag]
    
def getCS(jobDescription):
    #cs = ['CS_algorithm','CS_data structure','CS_data wrangling','CS_Data warehousing','CS_data mining','CS_VBA','CS_SAS','CS_distributed computing','CS_parallel computing','CS_XML','CS_HTML','CS_pandas']
    algorithm = dataStructure = dataWrangling = dataWarehousing = dataMining = vba =sas = distributingComputing = parallelComputing = formatConversion = html = pandas = 0
    if re.search('algorithm', jobDescription):
        algorithm = 1
    if re.search('data structure|structure', jobDescription ):
        dataStructure = 1
    if re.search('data wrangling|data preprocessing|data cleaning|wrangling', jobDescription):
        dataWrangling = 1
    if re.search('data mining', jobDescription):
        dataMining  = 1
    if re.search('vba', jobDescription):
        vba = 1
    if re.search('sas',jobDescription):
        sas = 1
    if re.search('distributed computing', jobDescription):
        distributingComputing = 1
    if re.search('parallel computing|multicore computing', jobDescription):
        parallelComputing = 1
    if re.search('xml|json|csv', jobDescription):
        formatConversion = 1
    if re.search('html|web development', jobDescription):
        html = 1
    if re.search('pandas', jobDescription):
        pandas = 1
    
    return [algorithm, dataStructure, dataWrangling, dataWarehousing, dataMining, vba, sas, distributingComputing, parallelComputing, formatConversion, html, pandas]

def getDataBase(jobDescription):
    #database = ['DB_sql', 'DB_nosql', 'DB_access', 'DB_teradata','DB_oracle database']
    sql = nosql = access = teradata = oracle = 0
    if re.search(' sql ', jobDescription):
        sql = 1
    if re.search('nosql', jobDescription):
        nosql = 1
    #CAUTION 
    #might generate bogus results here!!!
    if re.search (' access ', jobDescription):
        access = 1
    if re.search ('teradata', jobDescription):
        teradata = 1
    if re.search ('oracle database|oracle db', jobDescription):
        oracle = 1
    return [sql , nosql , access , teradata , oracle]

def getMachineLearnign(jobDescription):
    #ml = ['ML_NLP', 'ML_deep learning', 'ML_machine learning', 'ML_computer vision', 'ML_tensorflow', 'ML_scikit-learn]
    nlp = dp = ml = cv = tensor = scikit = 0
    if re.search('nlp|natural language processing', jobDescription):
        nlp = 1
    if re.search('dl|deep learning|cnn|rnn', jobDescription):
        dp = 1
    if re.search('machine learning|ml|aritificial intelligence|neural network', jobDescription):
        ml = 1
    if re.search('computer vision', jobDescription):
        cv = 1
    if re.search('tensorflow', jobDescription):
        tensor = 1
    if re.search('scikit-learn', jobDescription):
        scikit = 1
        
    return [nlp , dp , ml , cv , tensor , scikit]
def getSoftware(jobDescription):
    #software = ['SW_aws', 'SW_linux','SW_google cloud', 'SW_azure', 'SW_redshift', 'SW_git', 'SW_server','SW_api']
    aws = linux = gc = azure= redshift = git = server = api  = 0
    if re.search('aws|amazon web services', jobDescription):
        aws = 1
    if re.search('linux|unix|ubuntu', jobDescription):
        linux = 1
    if re.search('google cloud', jobDescription):
        gc = 1
    if re.search('azure', jobDescription):
        azure = 1
    if re.search('redshift', jobDescription):
        redshift = 1
    if re.search('server', jobDescription):
        server = 1
    if re.search('api', jobDescription):
        api = 1
        
    return [aws , linux , gc , azure , redshift , git , server , api]
def getBigData(jobDescription):
    #bigData = ['BD_hadoop','BD_scala','BD_apache','BD_hive','BD_D3','BD_big data' ,'BD_spark']
    hadoop = scala = apache = hive = d3 = spark = bd = spark = 0
    if re.search('hadoop', jobDescription):
        hadoop = 1
    if re.search('scala', jobDescription):
        scala = 1
    if re.search('apache', jobDescription):
        apache = 1
    if re.search('hive', jobDescription):
        apache = 1
    if re.search(' d3 ', jobDescription):
        hive = 1
    if re.search(' spark ', jobDescription):
        d3 = 1
    if re.search('big data', jobDescription):
        bd = 1
    if re.search('spark', jobDescription):
        spark = 1
    return [hadoop , scala , apache , hive,d3 , bd , spark ]
def getVisualization(jobDescription):
    #datavisualization = ['VISUAL_excel','VISUAL_tableau','VISUAL_ggplot','VISUAL_plotly','VISUAL_matplotlib','VISUAL_chartio','VISUAL_data visualization','VISUAL_powerpivot']
    excel = tableau = ggplot = plotly = matplotlib = chartio = dv = powerpivot = 0
    if re.search('excel', jobDescription):
        excel = 1
    if re.search('tableau', jobDescription):
        tableau = 1
    if re.search('ggplot', jobDescription):
        ggplot = 1
    if re.search('plotly', jobDescription):
        plotly = 1
    if re.search('matplotlib', jobDescription):
        matplotlib = 1
    if re.search('chartio', jobDescription):
        chartio = 1
    if re.search('data visualization', jobDescription):
        dv = 1
    if re.search('powerpivot', jobDescription):
        powerpivot = 1
    return [excel , tableau , ggplot , plotly , matplotlib , chartio , dv , powerpivot ]

def getExperience(jobDescription):
    experience = re.findall ('(\d)\+? ?years.+of.+experience',jobDescription)
    if experience == []:
        experience = ['no prior experience required/mentioned']
    else:
        if int(experience[0]) < 3:
            experience = ['1-2 years']
        elif int(experience[0]) < 6:
            experience = ['2-5 years']
        elif int(experience[0]) < 11:
            experience = ['6-10 years']
        else:
            experience = ['>10 years']
        
    return experience
def getDomainKnowledge(jobDescription):
    #ddomainKnowledge = ['DK_economics','DK_healthcare','DK_business','DK_finance','DK_management','DK_customer service','DK_marketing']
    economics = healthcare = business = finance = management = customerService = marketing = 0
    if re.search('economy|economics|econometrics', jobDescription):
        economics = 1
    if re.search('healthcare|medical', jobDescription):
        healthcare = 1
    if re.search('business|law|consult', jobDescription):
        business = 1
    if re.search('finace|bank|investment', jobDescription):
        finance = 1
    if re.search('management', jobDescription):
        management = 1
    if re.search('customer service', jobDescription):
        customerService = 1
    if re.search('marketing', jobDescription):
        marketing = 1
    return [economics , healthcare , business , finance , management , customerService , marketing]
def getCommunication(jobDescription):
    #communication = ['COMM_presentation','COMM_verbal','COMM_writting','COMM_interpersonal skills']
    presentation = verbal = writing = interpersonal = 0
    if re.search('presentation', jobDescription):
        presentation = 1
    if re.search('verbal', jobDescription):
        verbal = 1
    if re.search('writing', jobDescription):
        writing = 1
    if re.search('interpersonal', jobDescription):
        interpersonal = 1
    return [presentation , verbal , writing ,interpersonal]
def getDegree(jobDescription):
    
    if re.search('bachelor|b\.s\.', jobDescription):
        return ['Bachelor']
    elif re.search('master|m\.s\.', jobDescription):
        return ['Master']
    elif re.search('doctor|phd|ph\.d', jobDescription):
        return ['Doctor']
    else:
        return ['no degree requirement mentioned']
def getBackground(jobDescription):
    #background = ['computer science','data science','electrical engineering','statistics', 'mathematics' ,'physics','finance','informatics']
    cs = ds = ee = stats = math = phys  = finance = informatics = 0
    if re.search('computer science', jobDescription):
        cs = 1
    #CAUTION 
    #might generate bogus results here!!!
    if re.search('data science', jobDescription):
        ds = 1
    if re.search('electrical engineering', jobDescription):
        ee = 1
    if re.search('stats|statistics', jobDescription):
        stats = 1
    if re.search('math|mathematics', jobDescription):
        math = 1
    if re.search('physics', jobDescription):
        phys = 1
    if re.search('finance', jobDescription):
        finance = 1
    if re.search('informatics', jobDescription):
        informatics = 1

    return [cs , ds , ee , stats , math , phys  , finance , informatics ]


def main():
    inPath = '/Users/victorzhang/Desktop/preprocessed'
    outPath = '/Users/victorzhang/Desktop/extracted'
    csvFileName = 'finalPreprocessed.csv'
    outName = 'feature_extracted.csv'
    fileName = inPath + '/' + csvFileName
    df = loadCSV(fileName)
    answer = featureExtraction(df)
    saveCSV(outPath, answer,outName)
    
main()


    
    
    
    