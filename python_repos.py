import requests

# Set search parameters (easy to change the language)
chosen_language = 'javascript'

url = 'https://api.github.com/search/repositories'

# IMPROVEMENT 1: All search parameters are now in a clean 'search_params' dictionary.
# requests will automatically format and append them to the URL.
search_params = {
    'q': f'language:{chosen_language} stars:>10000',
    'sort': 'stars'
}

# Set headers as required by GitHub documentation
headers = {'Accept': 'application/vnd.github.v3+json'}

try:
    # Passing parameters via params= and added timeout=10 (wait max 10 seconds)
    r = requests.get(url, headers=headers, params=search_params, timeout=10)

    # Automatically raises an error if the status code is bad (e.g., 404 or 500)
    r.raise_for_status()

    print(f'Status Code: {r.status_code} (Success)')

    response_dict = r.json()
    print(f'Total {chosen_language.title()} repositories: {response_dict["total_count"]}')

    repo_dicts = response_dict['items']
    print(f'Repositories returned: {len(repo_dicts)}')

    print(f'\n--- TOP 5 POPULAR {chosen_language.upper()} REPOSITORIES ---')

    for repo_dict in repo_dicts[:5]:
        print('\n--------------------------------------------------')
        print(f"Name: {repo_dict['name']}")
        print(f"Owner: {repo_dict['owner']['login']}")
        print(f"Stars: {repo_dict['stargazers_count']}")
        print(f"Repository URL: {repo_dict['html_url']}")

        # Safe description extraction. If it doesn't exist, 'No description' will be displayed.
        description = repo_dict.get('description') or 'No description'
        print(f"Description: {description}")

except requests.exceptions.RequestException as e:
    # Catches internet issues, invalid URLs, or GitHub server downtime
    print(f"An error occurred while making the request: {e}")
