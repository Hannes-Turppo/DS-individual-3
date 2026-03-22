import xmlrpc.client
import datetime as dt

def get_topics(proxy):
  topics = proxy.get_topics()

  print("Available topics:")
  if len(topics) == 0:
    print("None")
  else:
    for topic in topics:
      print(f"- {topic}")
  print()

def get_notes(proxy):
  print("Get notes from a specific topic")
  topic = input("give a topic: ")
  notes = proxy.get_notes(topic)
  for note in notes:
    print()
    print(f"Note: {note["text"]}")
    print(f"Timestamp: {note["time"]}")
  print()

def send_note(proxy):
  print("Send a note to the server.")
  topic = input("Give a topic: ")
  text = input("Give a text: ")
  time = dt.datetime.now().isoformat(timespec="seconds")
  proxy.send_note({
    "topic":topic,
    "text":text,
    "time":time
    })
  print(f"sent topic \"{topic}\" to server with text:\n\"{text}\"")

def menu():
  print("Choose what to do:")
  print("1: Get available topics")
  print("2: Send note")
  print("3: Get notes from topic")
  print("0: Quit")
  choise = int(input("Choose option: "))
  return choise

def main():  
  with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
    while True:
      print() # Newline before new main loop
      choise = menu()
      print() # Newline before functionality
      if choise == 0:
        break
      if choise == 1:
        get_topics(proxy)
      if choise == 2:
        send_note(proxy)
      if choise == 3:
        get_notes(proxy)


if __name__=="__main__":
  main()
