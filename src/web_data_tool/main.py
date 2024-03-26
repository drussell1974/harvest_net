from setup import main as db_main
from task import Task

def setup():
    db_main()

def main():
    print('Hello world!')
    print('Welcome to web_data_tool package')


if __name__ == '__main__':
    main()

    print('Running task...')
    task = Task("http://www.google.com")
    
    task.run()

    print('Task completed')
    print('closing task...')
    task.close()
    print('Task closed!!!!!!!')

