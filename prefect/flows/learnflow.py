from prefect import flow

@flow
def my_fav_func():
    print("whats my fav number?")
    return 42

print(my_fav_func())