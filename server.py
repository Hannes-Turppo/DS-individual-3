from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from threading import Lock
import json


# class structures to store stuff in execution
class Note:
  def __init__(self, text, time):
    self.text = text
    self.time = time

class Notes:
  def __init__(self):
    self.notes = {}

  def add_note(self, topic, text, time):
    if topic not in self.notes:
      self.notes[topic] = []
    self.notes[topic].append(Note(text, time))

  def get_topics(self):
    return list(self.notes.keys())

  def get_notes(self, topic):
    if topic not in self.notes:
      return []
    return [{"text": note.text, "time": note.time} for note in self.notes[topic]]

  def to_dict(self):
    return {
      topic: [{"text": n.text, "time": n.time} for n in note_list]
      for topic, note_list in self.notes.items()
    }

  @staticmethod
  def from_dict(data):
    ns = Notes()
    for topic, note_list in data.items():
      ns.notes[topic] = [Note(n["text"], n["time"]) for n in note_list]
    return ns


class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
  daemon_threads = True
  allow_reuse_address = True

store_lock = Lock()

# Save old data to mockDB (file)
def save_data():
  with open("./storage.json", "w", encoding="utf-8") as storage_file:
    json.dump(note_store.to_dict(), storage_file)

# Retrieve old data
def init_storage():
  try:
    with open("./storage.json", "r", encoding="utf-8") as old_storage:
      data = json.load(old_storage)
      return Notes.from_dict(data)
  except (FileNotFoundError, json.JSONDecodeError):
    return Notes()


# functionality
def send_note(note_data):
  topic = note_data["topic"]
  text = note_data["text"]
  time = note_data["time"]

  with store_lock:
    note_store.add_note(topic, text, time)
    save_data()  # persist after each new note

  print(f"Stored note in topic '{topic}': {text}")
  return True

def get_topics():
  with store_lock:
    return note_store.get_topics()

def get_notes(topic):
  with store_lock:
    return note_store.get_notes(topic)


note_store = init_storage()
server = ThreadingXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(get_topics, "get_topics")
server.register_function(get_notes, "get_notes")
server.register_function(send_note, "send_note")
server.serve_forever()