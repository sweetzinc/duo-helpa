---
title: Duo-helper
emoji: 🦉
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.44.0
app_file: app.py
pinned: true
---

# Duo-helper🦉

## Intro
I am trying to learn claude code by creating this simple app!

## App-features
A minimal web UI that can complement language learning with Duolingo. It can be accessed from huggingface space with smartphone or tablet.
We are learning various target languages (German, French, Spanish, Italian) in English as the source language. 

Main functionalities are:
1. Word lookup. 
* If I put in an english word, show target language word with the gender and plural form (if exists)
* If I put in a target language word, show its gender and plural form.
* Have an option of looking at some example sentences. 

2. Grammar explanation. 
* User can ask a general grammar question.
* User can give a target language sentence or phrase that may or may not be correct, to see the corrected grammar and explanation. 

## Technical Framework
Because this is a learning project, I want to use things that are already familiar to me.
* Python based 
* Use "Gradio" and Gemini API
* Will be hosted on huggingface's private space. 