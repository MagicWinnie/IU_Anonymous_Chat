# Anonymous Chat
Simple anonymous chat project for Assignment 2 on Software Architecture course.  

## Team
Team 24:
- Gleb Bugaev (g.bugaev@innopolis.university)
- Nail Minnemullin (n.minnemullin@innopolis.university)
- Dmitriy Okoneshnikov (d.okoneshnikov@innopolis.university)
- Vladislav Bolshakov (v.bolshakov@innopolis.university)

## Project Structure
```
.
├── README.md
├── client                                     # this is where the client lies
│   ├── README.md
│   ├── main.py                                # entrypoint for the GUI client 
│   ├── modules
│   │   ├── __init__.py
│   │   ├── api.py                             # working with server API 
│   │   ├── message_queue.py                   # queue implementation for sending messages
│   │   ├── message_row.py                     # class representing one text message row in chat
│   │   ├── messages_list.py                   # class representing multiple text message rows
│   │   ├── schemas.py                         # Message Pydantic schema lies here
│   │   ├── texts.py                           # different texts that appear in GUI
│   │   └── utils.py                           # helper functions
│   └── requirements.txt
├── server                                     # this is where the server lies
│   ├── main.py                                # entrypoint for FastAPI
│   ├── models.py                              # MongoDB models
│   ├── repository.py                          # MongoDB queries
│   └── settings.py                            # server settings
└── tests                                      # this is where the test lie
    ├── helper.py                              # working with API
    ├── maintainability_index.py               # calculating the Maintainability Index
    ├── test_recoverability.py                 # testing responsibility
    └── test_time.py                           # testing response time
```