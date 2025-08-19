# Deploying to Heroku

This guide will help you deploy your Diabetic Retinopathy Detection application to Heroku so your followers can access it.

## Prerequisites

1. [Heroku account](https://signup.heroku.com/) (free tier available)
2. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
3. [Git](https://git-scm.com/downloads) installed

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 3. Create a Heroku App

```bash
heroku create your-app-name
```

Replace `your-app-name` with a unique name for your application.

### 4. Set Environment Variables

```bash
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
heroku config:set DEBUG=False
```

### 5. Add PostgreSQL Database

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### 6. Deploy to Heroku

```bash
git push heroku main
```

If your main branch is named `master` instead of `main`, use:

```bash
git push heroku master
```

### 7. Run Database Migrations (if needed)

```bash
heroku run python init_db.py
```

### 8. Open Your Application

```bash
heroku open
```

Or visit `https://your-app-name.herokuapp.com` in your browser.

## Sharing with Your Followers

Once deployed, you can share the URL (`https://your-app-name.herokuapp.com`) with your followers through:

- Social media posts
- Email newsletters
- Your personal website
- Direct messages

## Troubleshooting

### Viewing Logs

If you encounter issues, check the logs:

```bash
heroku logs --tail
```

### Common Issues

1. **Application Error**: Check logs for details
2. **H10 - App Crashed**: Usually due to configuration issues
3. **H14 - No Web Dynos Running**: Run `heroku ps:scale web=1`

## Maintaining Your Application

### Updating Your Application

After making changes locally:

```bash
git add .
git commit -m "Description of changes"
git push heroku main
```

### Monitoring Usage

Monitor your application's resource usage in the Heroku Dashboard to ensure you stay within free tier limits or upgrade as needed.

## Additional Resources

- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Heroku PostgreSQL](https://devcenter.heroku.com/articles/heroku-postgresql)
- [Heroku CLI Commands](https://devcenter.heroku.com/articles/heroku-cli-commands)