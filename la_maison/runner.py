import os
from scrapy.cmdline import execute

spider = "la_maison"

# log_directory = f"logs/scraping/{spider}"

# # Créer le répertoire de logs s'il n'existe pas
# if not os.path.exists(log_directory):
#     print(f"Directory not exist : {os.path.exists(log_directory)} created.")
#     os.makedirs(log_directory)
# else:
#     print(f"Directory already exist.")

# log_file = os.path.join(log_directory, f"{spider}.log")

try:
    # print(f"Clean the logs in file : {log_file}")
    # with open(log_file, 'w') as f:
    #     pass
    
    print(f"\nExecute spider : {spider}\n")
    
    execute([
        'scrapy',
        'crawl',
        spider,
        '-o',
        f'{spider}.csv'
        # '-s',
        # f'LOG_FILE={log_file}'
    ])
    
except SystemExit as e:
    print(f"\nError, exit script : {e}\n")
    pass

print(f"\nExtraction {spider} finish.\n")
