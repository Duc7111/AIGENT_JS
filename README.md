# AIGENT_JS

## Introduction
    AIGENeraTor is an application designed for creating AI or programs in general with drag-and-drop method. This application is currently created for educational purpose, so the perfomance of programs created with this aplication might have quite bad performance.

## Problem statement
    AI and Machine Learning (ML) have rapidly evolving recently and become a common and usefull tool in our daily life. However, these technology seem to be quite complicated, especially for newbie. We suffer these problems ourselves. Thus, we decide to implement an application to create AI pipelines so that everyone can take use of the basic level of AI as well as visualize them. We hope AIGENT can be a usefui tool to make learning, building, and using AI become an easy and enjoyable task for everyone.

## Architechture
    To create a drag-and-drop AI pipelines, we split them into modules, which is anything can work independently with some given input and return some output, do something, or both.

### Modules
    Modules consist of three main component: output buffer, which is design to hold and maintain value for asynchronus accesses; input buffer, which hold pointers to the corespond source: an output buffer of another module; and a run method, define how a module compute, act, and map input value to output value. This design allow modules to work all by themselves, provide good modularity.

### Pipeline
    To make it easier for users to build bigger and bigger applications, we implement a Pipeline as if it is a module. Pipelines inherith all nature of modules with additional infomation about the modules that the pipeline has. Pipelines run by activate all modules and let them run in multi-thread. This allow us to maximize the flexablity of the pipeline with a simple design. However, this design heavily effect the performance of the pipeline, especially for feed-foward pipelines consist of many modules.  

##