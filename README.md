# AIGENT_JS

## Introduction
AIGENeraTor is an application designed for creating AI or programs in general with drag-and-drop method. This application is currently created for educational purpose, so the perfomance of programs created with this aplication might have quite bad performance.

## Problem statement
AI and Machine Learning (ML) have rapidly evolving recently and become a common and usefull tool in our daily life. However, these technology seem to be quite complicated, especially for newbie. We suffer these problems ourselves. Thus, we decide to implement an application to create AI pipelines so that everyone can take use of the basic level of AI as well as visualize them. We hope AIGENT can be a usefui tool to make learning, building, and using AI become an easy and enjoyable task for everyone.

## Usecase Diagram
USECASE DIAGRAM GO HERE

## Class Diagram

<picture>
 <source media="(prefers-color-scheme: dark)" srcset="AIGENT_ClassDiagram.drawio.svg">
 <source media="(prefers-color-scheme: light)" srcset="AIGENT_ClassDiagram.drawio.svg">
 <img alt="YOUR-ALT-TEXT" src="AIGENT_ClassDiagram.drawio.svg">
</picture>

## Architechture
Our program consist of two parts, which can work independently, frontend and backend. While frontend is coded with python, backend is implemented with Electron, a popular Node.js framework for desktop development that have web like syntax - which not seem to help at all. These two parts communicate with each other purely by json strings sended through TCP/IP sockets

### Backend
To create a drag-and-drop AI pipelines, we split them into modules, which is anything can work independently with some given input and return some output, do something, or both.

#### Modules
Modules consist of three main component: output buffer, which is design to hold and maintain value for asynchronus accesses; input buffer, which hold pointers to the corespond source: an output buffer of another module; and a run method, define how a module compute, act, and map input value to output value. This design allow modules to work all by themselves, provide good modularity.

<p align = "center">
  <picture>
   <source media="(prefers-color-scheme: dark)" srcset="Module.drawio.svg">
   <source media="(prefers-color-scheme: light)" srcset="Module.drawio.svg">
   <img alt="YOUR-ALT-TEXT" src="Module.drawio.svg">
  </picture>  
</p>

Our backend is designed to allow developers to easily scale built-in modules. Just implement your own module following the implemented modules we provide in to the available files or a new python file and place it in python folder and it will work fine. However, our frontend has not support this feature yet due to difficulties in file reading and text processing. 

#### Pipeline
To make it easier for users to build bigger and bigger applications, we implement a Pipeline as if it is a module. Pipelines inherith all nature of modules with additional infomation about the modules that the pipeline has. Pipelines run by activate all modules and let them run in multi-thread. This allow us to maximize the flexablity of the pipeline with a simple design. However, this design heavily effect the performance of the pipeline, especially for feed-foward pipelines consist of many modules.  

<p align = "center">
  <picture>
   <source media="(prefers-color-scheme: dark)" srcset="Pipeline.drawio.svg">
   <source media="(prefers-color-scheme: light)" srcset="Pipeline.drawio.svg">
   <img alt="YOUR-ALT-TEXT" src="Pipeline.drawio.svg">
  </picture>  
</p>

A pipeline can be saved, and because pipelines are also modules, it can be added into other pipelines. Hence, our program allow users to build up large pipeline by gradually building smaller pipelines

### Frontend
#### Use case diagram
<p align = "center">
  <picture>
   <source media="(prefers-color-scheme: dark)" srcset="usecase.drawio.svg">
   <source media="(prefers-color-scheme: light)" srcset="usecase.drawio.svg">
   <img alt="YOUR-ALT-TEXT" src="usecase.drawio.svg">
  </picture>  
</p>

The diagram visually depicts:

User Interactions: How users (actors) can interact with the system to manage pipelines.

Functionalities: Key functionalities available to users, including creating directories, searching pipelines, managing projects, building/deleting pipelines, and exporting/importing data.

Relationships: Connections between functionalities, such as nested actions and optional extensions.
This use case diagram provides a clear understanding of user interaction capabilities within the pipeline management system.
## Key Features
KEY FEATURE GO HERE
1. Drag and Drop Modules:
Our platform offers an intuitive drag-and-drop interface that allows users to seamlessly add modules to their workspace. Users can effortlessly move these modules around the workspace, arranging them in any configuration that suits their workflow.

2. Zoom and Pan:
To enhance user experience, the workspace supports zooming in and out, providing users with the flexibility to focus on specific modules or get an overview of the entire project. Additionally, users can pan across the workspace to navigate their modules easily.

3. Flexible Module Positioning:
Users can position modules anywhere within the workspace, giving them complete control over the layout. This feature ensures that users can organize their workspace in the most efficient and personalized manner.

4. Connectable Gates:
Each module comes equipped with gates that can be connected to gates of other modules. This allows users to create complex workflows by linking modules together to perform specific tasks or functions. The connectivity between modules enables the execution of customized operations tailored to the user's requirements.
## Contributers
Duc7111 - Duc7111: Backend developer

TringuyenCoding - TringuyenCoding: Frontend developer
