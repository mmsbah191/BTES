# BTES - Booking Tickets Events System10

BTES (Booking Tickets Events System) is a web-based application designed to allow users to easily view, search, and book tickets for various events. It provides a user-friendly interface for managing event bookings and includes features like refunds, payment processing, and admin event management.

## Prerequisites

Before you begin, make sure you have the following software installed:

- **Python 3.12.0**: get last version by `python.exe -m pip install --upgrade pip`
- **Browser**:run the project on your local web server.
- **Git**:(optional)vcs to sync and pull & push updates if you want.

## Installation

1. **where you want Installation Btes project**:

   open git bash command or ps write yourpath  Let's say at desktop

```bash
cd C:/Users/%USERPROFILE%/Desktop
```

2. **Clone the repository**:

```bash
 git clone https://github.com/mmsbah191/BTES.git
```

3.**Opthinal**

```bash
 cd BTES
```

```bash
git branch -m main
```

## Usage & run in browser

by terminal or powershell(ps) or git, change %USERPROFILE% with your username like

1. **go to the project directory**:

   ```bash
   cd C:/Users/%USERPROFILE%/Desktop/BTES
   ```
2. **Open your editor or Ide from current path**
   if VsCode `code .` or click riht in files then alot option then open BTES with vscode
   then by your editor go to built in terminal with `ctrl+`` or `ctrl+ذ` or click terminal button in navbar option
3. **Activate the virtual environment**
   (optinal try discard it) sometimes your terminal editor Activate automatic

   - **On Windows powershell**:
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS and Linux**:
     ```bash
     source venv/bin/activate
     ```
4. **Run the Django development server**:
   from btes directory

   ```bash
   py manage.py runserver
   ```
5. **Open a web browser and go to**:
   This will open the application on your local web server.

   pages links: ```http://127.0.0.1:8000```

   databases link/admin panel link: ```http://127.0.0.1:8000/admin/```

**Notes:**
for login in database create username if you don't have one get one by terminal write.

```bash
py manage.py createsuperuser
```

## Features

- User registration and login
- Event search and filtering
- Ticket booking with integrated payment systems
- Refund processing (within 24 hours for logged-in users)
- Admin panel for managing events and viewing summaries
  Here's a more detailed guide for the **Contributing** section, explaining step-by-step how to use Git and GitHub for collaboration:

## Contributing

Follow these steps to contribute to the project:

### 1. Fork the Repository

- First, click on **Fork** in the top-right corner to create a copy of the repository under your GitHub account.
  **prefer with same name BTES.**

### 2. Clone the Repository

- Clone your forked repository to your local machine by running the following command:

  ```bash
  cd desktop
  ```

  ```bash
  git clone https://github.com/mmsbah191/BTES.git
  ```

### 3. Navigate to the Project Directory

- Move into the project directory:
  ```bash
  cd BTES
  ```

### 4. Set Upstream to your forkes Repository

- To keep your forked repository in sync with the your forked, add the forked repository as the origin remote:

  ```bash
  git remote add origin https://github.com/!!usernamegithup!!/BTES.git
  ```

  **prefer with origin name small letter for Original Repository.**

### (optional)(advance)Set Upstream to Original Repository

- To keep your forked repository in sync with the original, add the original repository as the upstream remote:

  ```bash
  git remote add upstream https://github.com/mmsbah191/BTES.git
  ```

  **prefer with upstream name small letter  for Original Repository.**

### 5. First command before push updates to github

```bash
git branch -m main
```

```bash
git config --global user.name "yourName"
```

```bash
git config --global user.email "yourMail@g.c"
```

```bash
git pull origin main --allow-unrelated-histories
```

for varity & link GitHub with your git bash:

```bash
git push -u origin main
```

### 6. Start Coding & do changes

- Make changes or add new code. As you work, you can check the status of modified files using:
  ```bash
  git status
  ```

### 7. Stage and Commit Changes

- Once you’re ready to save your changes, stage the files you want to commit:
  ```bash
  git add .
  ```
- Commit your changes with a descriptive message:
  ```bash
  git commit -m "Add a description of what you did"
  ```

### 8. Push Changes to Your Branch

- Push your changes to the branch on your forked GitHub repository:
  ```bash
  git push -u origin main
  ```
- someties you need fetch & pull updates before push
  ```bash
  git fetch main
  git pull origin main --allow-unrelated-histories
  ```

### 9.(optional)if you want Pull Updates from the Original Repository (Upstream)

- Before submitting a pull request, make sure your branch is up-to-date with the original repository by fetching and merging any changes:
  ```bash
  git fetch upstream
  git checkout main
  git merge upstream/main
  ```

### 10. Submit a Pull Request from sync at your repository forked

- After pushing all your changes, go to your forked repository on GitHub, and you’ll see an option to submit a pull request (PR). Follow the prompts to create the PR to the original repository’s main branch.

## Contributors

- **Mohamed Mesbah Ibrahim**
- **May moktar algallai**

## Acknowledgments

Special thanks to Dr. Ali AbuRas for his guidance and support in CS315.
