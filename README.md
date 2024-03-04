
Welcome to, 

# Application Manual - Zinc Flake

Live link - 

![Screenshot]

## Introduction

The manual includes the following: 
• Information and guidance on the zinc flake product portfolio; 
• Instructions for quality control of the systems

## Table of Contents

- [Project Goals](#project-goals)
- [User Experience - Jesse James Garrett's 5 Planes Model of UX](#user-experience-jesse-james-garret's-5-planes-of-ux)
- [Scope](#scope)
- [Design](#design)
- [Features](#features)
- [Technologies](#technologies-used)
- [Testing](#testing)
- [Bugs](#bugs)
- [Deployment](#deployment)
- [Clone a repository code locally](#clone-a-repository-code-locally)
- [Forking in GitHub](#forking-in-github)
- [Credits](#credits)

## Project Goals

This application ensures that the transformation of the ZN-FL based products application manual into a web app not only meets current digital standards but also provides a superior user experience, leveraging the strengths of digital platforms to enhance accessibility, understanding, and application of the manual's contents.

- __User Goals__
    - Not only a resourceful manual but also as an interactive platform where users can engage with the content and each other, enhancing the overall UX.
    - Supports a more personalised and community-driven approach to content consumption and feedback.

- __Site Owner Goals__
    - The primary objective is to provide easy access to the application manual with enhanced navigability, searchability, and interactivity. 
    - Secondary objectives include offering updated information, and technical support.
  

## User Experience - Jesse James Garrett's 5 Planes Model of UX

- __Strategy  Layer__
- Site Owner Goals:
    - The primary objective is to provide easy access to the application manual with enhanced navigability, searchability, and interactivity. 
    - Secondary objectives include offering updated information, and technical support.
- User Goals:
    - Not only a resourceful manual but also as an interactive platform where users can engage with the content and each other, enhancing the overall UX.
    - Supports a more personalised and community-driven approach to content consumption and feedback. 

- __Scope Layer__
- Functional Requirements:
    - Search functionality to quickly find topics.
    - User accounts for saving favourites and comments.
    - Accessibility features, including screen reader compatibility, and alternative text for images.
- Content Requirements:
    - Conversion of the manual content into digital format, organized by chapters and sections as listed.
    - Addition of multimedia content for demonstration.
 
- __Structure Layer__
- Interaction Design:
    - Simplified navigation through a clear, hierarchical structure.
    - Responsive design to adapt to various devices and screen sizes.
    - Interactive elements such as dropdown menus for each product category, accordion panels for FAQs, and modals for quick tips.
- Information Architecture:
    - A logical grouping of content into categories and subcategories as per the manual's chapters.
    - A table of contents with hyperlinks for easy access to specific sections.
    - Breadcrumbs for easy tracking of user's position within the manual.
 
- __Skeleton Layer__
- Interface Design:
    - Clean and intuitive layout with a focus on readability (adequate font sizes and contrasts).
    - Consistent use of icons and colour coding to denote different sections or types of information.
- Navigation Design:
    - Fixed or sticky menu for the main navigation.
    - A back-to-top button for easy navigation on longer pages.
    - Search bar accessible from all pages.
- Information Design:
    - Use of charts, infographics, and bullet points to present complex information in an easily digestible format.
    - Tooltip explanations for technical terms or abbreviations.

- __Surface Layer__
- Visual Design:
    - Adherence to the brand’s colour scheme and typography to maintain consistency and brand recognition.
    - Use of whitespace to avoid clutter and focus attention on content.
    - High-quality images where necessary to demonstrate processes or end results.
 
- __Accessibility & Inclusivity__
- Visual Design:
    - Compliance with WCAG (Web Content Accessibility Guidelines) to cater to users with disabilities.
    - Text alternatives for non-text content, meaningful sequence, and navigation accessible through a keyboard.
    - Use ARIA (Accessible Rich Internet Applications) labels for interactive elements.
 

## Scope 
Epics, user stories, and acceptance criteria are written following agile development practices.
This structure helps in organising the development process, ensuring all user needs and business objectives are met systemtically. 

- __User Account Management__
- __Content Management System__
- __Search Functinality__
- __User Interaction and Feedback__
- __User Engagement and Personalisation__
- __Accessibility and Compliance__
- __Multimedia Content Integration__

The development of the web app is user-focused, prioritising ease of access, interaction, and continuous improvement based on user feedback. 


[Back to Table of Contents](#table-of-contents)

## Design

- __Design Choices__
    - Simple, text-based interface for easy navigation.
    - Clear and concise instructions for user guidance.
    - Strategic use of colors to enhance user experience.

- __Flowchart__
    - The game flow was planned with a detailed flowchart, ensuring a logical progression and a smooth user experience. The first screenshot illustrates the navigation logic and the main menu loop.

    - The second screenshot illustrates the game loop. 

[Back to Table of Contents](#table-of-contents)

## Features

#### Welcome screen

- Users are greeted with the game name and instructions on how to start.


[Back to Table of Contents](#table-of-contents)

### __Technologies Used__

- Python: The primary language for game development.
- GitHub: Used to store and manage the project's code.
- Gitpod/VSCode: The integrated development environment for coding and version control.
- Git: Employed for version control via the VSCode terminal.
- Heroku: Platform for deploying and managing the application.

[Back to Table of Contents](#table-of-contents)

## Testing

#### Python Validation 

- All Python modules were thoroughly tested and validated using CI Python linters to ensure code quality and adherence to Pythonic conventions PEP8.
- Errors were all related to four main issues, trailing white spaces, line length, indentation levels and spaces around keyword/parameter "="

##### E501 line too long (117 > 79 characters)
- **Cause:** Lines exceeding the maximum recommended length of 79 characters, affecting readability.
- **Solution:** Broke long lines into shorter ones using parentheses, line continuation character `\`, and reformatting.

- Errors before fixing

- All five modules: run.py, gameboard.py, ship.py, utils.py, and leaderboard.py after addressing the issues above, the code is now more standardized, readable, and maintainable, adhering to Python's PEP8 styling guide.

#### Validation Error-based Fixes
- Navigation menu validation, welcome screen

- Navigation menu validation, game rules screen

- Navigation menu validation, change difficulty screen

- Game loop validation, out of range coordinates

- Game loop validation, invalid input format


[Back to Table of Contents](#table-of-contents)

## Manual Testing

| Section Tested | Input To Validate | Expected Outcome | Actual Outcome | Pass/Fail |
| -------------- | ----------------- | ---------------- | -------------- | --------- |
| Welcome screen | Name Entry        | Acceptance of alphanumeric characters for the player name | As expected | Pass      |
| Gameplay       | Coordinate Input  | Acceptance of valid board coordinates with appropriate action (hit/miss) | As expected | Pass      |
| Game Over      | N/A               | Display of the final game state and options to play again or quit | As expected | Pass      |
| Leaderboard    | N/A               | Accurate reflection of wins and losses | As expected | Pass      |

[Back to Table of Contents](#table-of-contents)

## Bugs
- Throughout the development process, several bugs were encountered and resolved. Below is a list of notable bugs and their resolutions:

| Bug | Fix |
| --- | --- |
| Multiple hits on the same ship coordinate | Adjusted `take_shot` method to flag coordinates that have already been hit |
| Incorrect leaderboard update | Corrected logic in the `update_score` method to properly increment wins and losses |
| Game prematurely ending | Ensured that the game checks for all ships being sunk before declaring the game over |

- Some bugs are still being worked on:

| Bug | Status |
| --- | ------ |
| Game speed inconsistency | In progress - adjusting typing effect speeds |


[Back to Table of Contents](#table-of-contents)

## Deployment

### Version Control

- The Battleship game was developed using Visual Studio Code and version controlled via Git and GitHub.
- I used Visual Studio code editor to create my site and pushed to GitHub to the remote repository.
- The following git commands were used in development to push code to the remote repo:
- git add - This command was used to add the file(s) to the staging area before they are committed.
- git commit -m “commit message” - This command was used to commit changes to the local repository queue ready for the final step.
- git push - This command was used to push all committed code to the remote repository on github.

### Deployment

- The application was deployed to Heroku, making it accessible to users online.
- The Battleship game, being a command-line application, is hosted on Heroku, allowing users to play it directly from their browsers.
- Deploying on Heroku:
- A Procfile and requirements.txt file were created to specify the commands that are executed by the app on startup.
- The app was linked to the GitHub repository for automatic deployment upon updates to the main branch.
- The live link to play the game is available here: 
Live link - [Battleship](https://python-project-bs-game-0c8cb15b2dbe.herokuapp.com/)

### Clone a repository code locally

- Step-by-step guide on how to clone the repository locally.
- To clone the Battleship repository code to your local machine:
- Access the repository URL of the remote repository you want to clone.
- Click on the green 'Code' button.
- Under 'HTTPS', copy the repository link.
- In your IDE, open the terminal.
- Paste the repository link into the terminal.
- Git will download all the files from the remote repository to your local machine. Once the process is finished, you'll have a local copy of the repository.

[Back to Table of Contents](#table-of-contents)

### Forking in GitHub

- Instructions on how to fork the repository for personal modification and contribution:
- Go to the GitHub repository: 
[Battleship Repository](https://github.com/OSawani/python-project-3).
- Click the 'Fork' button on the top right corner of the repository page.
- You will be redirected to your fork of the repository. This version is a copy of the original.
- You can now make changes, add features, fix issues, or modify the code within your fork. 
- These changes do not affect the original repository.
- If you want to propose your changes to the original project, create a "Pull Request." 
- The original repository owner can then review and decide whether to merge your contributions.

[Back to Table of Contents](#table-of-contents)

## Credits
Thanks to my mentor Medale Oluwafemi for his guidance and support. 

### Design

- Design inspired by 

## Acknowledgements

- Thanks to the Python community, Heroku, and beta testers.

[Back to Table of Contents](#table-of-contents)

---
