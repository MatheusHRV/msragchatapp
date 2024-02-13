# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 11:32:00 2024

@author: Matheus Vicente, @MatheusHRV
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from docx import Document
import re
from docx2pdf import convert

url = "https://www.tudoreceitas.com/receitas-brasileiras"
option = Options()
option.headlers = True 

driver = webdriver.Firefox(service=Service(executable_path=GeckoDriverManager().install()))

href_list = []
categoria_list = []
title_list = []
guests_list = []
time_list = []
meal_list = []
difficulty_list = []
additional_list = []
ingredients_list = []
utensils_list = []
howto_list = []

for i in range(1): #1, 23
    driver.get(f"https://www.tudoreceitas.com/receitas-brasileiras/{i}")
    elm_categoria = driver.find_elements(By.CLASS_NAME,'etiqueta')
    for value in elm_categoria:
        categoria_list.append(value.text)
    
    for b in range(4, 56):
        try:
            elm_href1 = driver.find_element(By.XPATH,f'/html/body/div/div[3]/div[1]/div[3]/div[1]/div/div[{b}]/a') # 3 a 55
            href_list.append(elm_href1.get_attribute('href'))
        except NoSuchElementException:
            print(f"pulou em B {b}")
            continue

for p in range(2, 23): #2, 23
    driver.get(f"https://www.tudoreceitas.com/receitas-brasileiras/{p}")
    elm_categoria = driver.find_elements(By.CLASS_NAME,'etiqueta')
    for value in elm_categoria:
        categoria_list.append(value.text)    
        
    for c in range(3, 56):
        try:
            elm_href = driver.find_element(By.XPATH,f'/html/body/div/div[3]/div[1]/div[2]/div[1]/div/div[{c}]/a') # 3 a 55
            href_list.append(elm_href.get_attribute('href'))
        except NoSuchElementException:
            print(f"pulou em C {c}")
            continue

len_href = len(href_list)
count = 0
for href in href_list:
    
    print(f"Iteração {count} de {len_href}")
    driver.get(href)
    try:
        title = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/h1').text
        title_list.append(title)
    except NoSuchElementException:
        title = 'Não informado'
        title_list.append(title)
        print('Erro title')
        pass
    
    try:
        guests = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[1]/span[1]').text
        guests_list.append(guests)
    except NoSuchElementException:
        guests = 'Não informado'
        guests_list.append(guests)
        print('Erro guests')
        pass
     
    try:
        time_elm = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[1]/span[2]').text
        time_list.append(time_elm)
    except NoSuchElementException:
        time_elm = 'Não informado'
        time_list.append(time_elm)
        print('Erro time')
        pass
     
    try:
        meal = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[1]/span[3]').text
        meal_list.append(meal)
    except NoSuchElementException:
        meal = 'Não informado'
        meal_list.append(meal)
        print('Erro meal')
        pass
    
    try:
        difficulty = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[1]/span[4]').text
        difficulty_list.append(difficulty)
    except NoSuchElementException:
        difficulty = 'Não informado'
        difficulty_list.append(difficulty)
        print('Erro diff')
        pass
    
    try:
        additional = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[2]').text
        additional_list.append(additional)
    except NoSuchElementException:
        additional = 'Não informado'
        additional_list.append(additional)
        print('Erro add')
        pass
    
    ing_table_elm = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[4]/ul')
    
    ingredients = ing_table_elm.find_elements(By.TAG_NAME,'li')
    ing_sublist = []
    for index, ing_values in enumerate(ingredients):
        ing_sublist.append(ing_values.text)
        
    ingredients_list.append(ing_sublist)
    
    try:
        utensils = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/article/div[2]/div[4]/div[6]/ul/li').text
        utensils_list.append(utensils)
    except NoSuchElementException:
        utensils = 'Não informado'
        utensils_list.append(utensils)
        print('Erro utensils')
        pass

    howto = driver.find_elements(By.TAG_NAME,'p')
    howto_sublist = []
    for howto_values in howto:
        howto_sublist.append(howto_values.text)
        
    howto_list.append(howto_sublist[:-2])
    

    value_cat = str(categoria_list[count])

    value_ing = str(ingredients_list[count])

    value_howto = str(howto_list[count])

    pattern = r"\[|\]|\'"
    value_cat = re.sub(pattern, "", value_cat)
    value_ing = re.sub(pattern, "", value_ing)
    value_howto = re.sub(pattern, "", value_howto)
    
    doc = Document()
    
    variables = ["Título da receita (recipe title): " + title, 
                 "Categoria (category): " + value_cat, 
                 "Serve (guests): " + guests, 
                 "Tempo de preparação (time): " + time_elm, 
                 "Refeição (meal): " + meal, 
                 "Dificuldade (difficulty): " + difficulty, 
                 additional, 
                 "Ingredientes (ingredients): " + value_ing, 
                 "Utensilhos (utensils): " + utensils, 
                 "Como preparar (how to do it): " + value_howto]

    for var in variables:
        doc.add_paragraph(var)

    doc.save(f"{title}.docx")
    
    convert(f"{title}.docx", f"{title}.pdf")
    
    #time.sleep(1)
    count += 1
    
driver.quit()