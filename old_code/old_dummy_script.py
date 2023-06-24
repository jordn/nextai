import os
from typing import List

from ai_utils.simplechat import ChatConversation

print("hey")

system = """
You are BabyAGI, a helpful AI.
Your job is to complete an objective for the user.
You are very forgetful, so you must occasionally write down your thoughts/insights/plans in a notebook.
"""

objective = "There's a codebase in the current directory. Tell the user how it works (in plain English). Then write a README.md file that explains how it works."

notebook = """
Initial note:
I should probably make a plan of how to complete my objective. (and write it down in my notebook)
"""

def user():
    return f"""
Your objective is "{objective}".

What's in your notebook right now:
------------------
{notebook}
------------------

Now work towards your objective (plan, act, etc).
"""

## FUNCS

# dummy filesystem

fs = {
    "heapsort.py":"""
# heapify
# max nodes should go to root
# uses only "greater than"

# given a node pointing to two heaps, ensure that the node forms a heap.
# cmp means "subtract"
id = lambda a,b: a-b
def heapify(arr,idx,max_len,cmp=id):
if idx>= max_len: return
n = arr[idx]
l = arr[2*idx+1] if 2*idx+1 < max_len else n
r = arr[2*idx+2] if 2*idx+2 < max_len else n

if cmp(l,n)>0 or cmp(r,n)>0:
    swap_idx,swap_val = (2*idx+1,l) if cmp(l,r)>0 else (2*idx+2,r)
    arr[swap_idx] = n
    arr[idx] = swap_val
    heapify(arr,swap_idx,max_len,cmp)

# heapifies its way up the heap. this means only checking if node > parent, swapping if necessary
def reverse_heapify(arr,idx,cmp=id):
if idx==0: return
p_idx = (idx-1)//2
n = arr[idx]
p = arr[p_idx]

if cmp(n,p)>0:
    arr[p_idx],arr[idx] = arr[idx],arr[p_idx]
    reverse_heapify(arr,p_idx,cmp)

def heapsort(arr,cmp=id):
for i in range(len(arr))[::-1]:
    heapify(arr,i,len(arr),cmp)

for num_sorted in range(len(arr)):
    arr[0], arr[-1-num_sorted] = arr[-1-num_sorted], arr[0]
    heapify(arr,0,len(arr)-num_sorted-1,cmp)

return arr

heapsort([])

if __name__ == "__main__":
print(heapsort([34,2,5,543,3,5,2,8,5,3,4,9,2,6]))
""",
    "pqueue.py":"""
from heapsort import *
from quick_lookup_list import QuickLookup

reverse = lambda cmp: lambda a,b:cmp(b,a)

# O(logn) push, O(logn) popmin, O(logn) promote
class PQueue:
def __init__(self,cmp=id):
    self.heap = []
    self.set = set()
    self.cmp = reverse(cmp)
def __len__(self):
    return len(self.heap)
def __contains__(self,el):
    return el in self.set
def peek(self):
    assert len(self.heap) > 0, "Can't peek into empty pqueue"
    return self.heap[0]
def push(self,el):
    assert el not in self,"Can't push--is already in heap"
    self.heap.append(el) # use a max-heap as a min-heap
    self.set.add(el)
    reverse_heapify(self.heap,len(self.heap)-1,self.cmp)
def popmin(self):
    assert len(self)>0, "Cannot pop from empty pqueue"

    self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
    ret = self.heap.pop()
    heapify(self.heap,0,len(self.heap),self.cmp)
    return ret
# This exclusively makes els *higher priority*--i.e. their number becomes smaller
def promote(self,el):
    idx = self.heap.index(el)
    assert idx>=0,"Element to promote was not found"
    reverse_heapify(self.heap,idx,self.cmp)

# vals = {
#     "a":1,
#     "b":5,
#     "c":-5,
#     "d":-4
# }
# pqueue = PQueue(lambda a,b:vals[a]-vals[b])
# pqueue.push("a")
# pqueue.push("b")
# pqueue.push("c")
# pqueue.push("d")
# vals["d"]=-6
# pqueue.promote("d")
# print(pqueue.popmin(),pqueue.popmin())
""",
    "social-media-scraping":{"schema.json":"""
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/Tweet",
    "definitions": {
        "Tweet": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "entryId": {
                    "type": "string"
                },
                "sortIndex": {
                    "type": "string"
                },
                "content": {
                    "$ref": "#/definitions/Content"
                }
            },
            "required": [],
            "title": "Tweet"
        },
        "Content": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "entryType": {
                    "type": "string"
                },
                "__typename": {
                    "type": "string"
                },
                "itemContent": {
                    "$ref": "#/definitions/ItemContent"
                }
            },
            "required": [],
            "title": "Content"
        },
        "ItemContent": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "itemType": {
                    "type": "string"
                },
                "__typename": {
                    "type": "string"
                },
                "tweet_results": {
                    "$ref": "#/definitions/TweetResults"
                },
                "tweetDisplayType": {
                    "type": "string"
                },
                "ruxContext": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "ItemContent"
        },
        "TweetResults": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "result": {
                    "$ref": "#/definitions/TweetResultsResult"
                }
            },
            "required": [],
            "title": "TweetResults"
        },
        "TweetResultsResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "__typename": {
                    "type": "string"
                },
                "rest_id": {
                    "type": "string"
                },
                "has_birdwatch_notes": {
                    "type": "boolean"
                },
                "core": {
                    "$ref": "#/definitions/PurpleCore"
                },
                "edit_control": {
                    "$ref": "#/definitions/EditControl"
                },
                "is_translatable": {
                    "type": "boolean"
                },
                "views": {
                    "$ref": "#/definitions/Views"
                },
                "source": {
                    "type": "string"
                },
                "quoted_status_result": {
                    "$ref": "#/definitions/QuotedStatusResult"
                },
                "legacy": {
                    "$ref": "#/definitions/FluffyLegacy"
                },
                "quick_promote_eligibility": {
                    "$ref": "#/definitions/QuickPromoteEligibility"
                }
            },
            "required": [],
            "title": "TweetResultsResult"
        },
        "PurpleCore": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "user_results": {
                    "$ref": "#/definitions/PurpleUserResults"
                }
            },
            "required": [],
            "title": "PurpleCore"
        },
        "PurpleUserResults": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "result": {
                    "$ref": "#/definitions/PurpleResult"
                }
            },
            "required": [],
            "title": "PurpleUserResults"
        },
        "PurpleResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "__typename": {
                    "type": "string"
                },
                "id": {
                    "type": "string"
                },
                "rest_id": {
                    "type": "string",
                    "format": "integer"
                },
                "affiliates_highlighted_label": {
                    "$ref": "#/definitions/AffiliatesHighlightedLabel"
                },
                "is_blue_verified": {
                    "type": "boolean"
                },
                "profile_image_shape": {
                    "type": "string"
                },
                "legacy": {
                    "$ref": "#/definitions/PurpleLegacy"
                }
            },
            "required": [],
            "title": "PurpleResult"
        },
        "AffiliatesHighlightedLabel": {
            "type": "object",
            "additionalProperties": false,
            "title": "AffiliatesHighlightedLabel"
        },
        "PurpleLegacy": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "created_at": {
                    "type": "string"
                },
                "default_profile": {
                    "type": "boolean"
                },
                "default_profile_image": {
                    "type": "boolean"
                },
                "description": {
                    "type": "string"
                },
                "entities": {
                    "$ref": "#/definitions/PurpleEntities"
                },
                "fast_followers_count": {
                    "type": "integer"
                },
                "favourites_count": {
                    "type": "integer"
                },
                "followers_count": {
                    "type": "integer"
                },
                "friends_count": {
                    "type": "integer"
                },
                "has_custom_timelines": {
                    "type": "boolean"
                },
                "is_translator": {
                    "type": "boolean"
                },
                "listed_count": {
                    "type": "integer"
                },
                "location": {
                    "type": "string"
                },
                "media_count": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "normal_followers_count": {
                    "type": "integer"
                },
                "pinned_tweet_ids_str": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "possibly_sensitive": {
                    "type": "boolean"
                },
                "profile_image_url_https": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ],
                    "qt-uri-extensions": [
                        ".jpg"
                    ]
                },
                "profile_interstitial_type": {
                    "type": "string"
                },
                "screen_name": {
                    "type": "string"
                },
                "statuses_count": {
                    "type": "integer"
                },
                "translator_type": {
                    "type": "string"
                },
                "url": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                },
                "verified": {
                    "type": "boolean"
                },
                "withheld_in_countries": {
                    "type": "array",
                    "items": {}
                },
                "profile_banner_url": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                }
            },
            "required": [],
            "title": "PurpleLegacy"
        },
        "PurpleEntities": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "description": {
                    "$ref": "#/definitions/Description"
                },
                "url": {
                    "$ref": "#/definitions/Description"
                }
            },
            "required": [],
            "title": "PurpleEntities"
        },
        "Description": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "urls": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/URL"
                    }
                }
            },
            "required": [],
            "title": "Description"
        },
        "URL": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "display_url": {
                    "type": "string"
                },
                "expanded_url": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                },
                "url": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                },
                "indices": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                }
            },
            "required": [],
            "title": "URL"
        },
        "EditControl": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "edit_tweet_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "editable_until_msecs": {
                    "type": "string"
                },
                "is_edit_eligible": {
                    "type": "boolean"
                },
                "edits_remaining": {
                    "type": "string",
                    "format": "integer"
                }
            },
            "required": [],
            "title": "EditControl"
        },
        "FluffyLegacy": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "bookmark_count": {
                    "type": "integer"
                },
                "bookmarked": {
                    "type": "boolean"
                },
                "created_at": {
                    "type": "string"
                },
                "conversation_id_str": {
                    "type": "string"
                },
                "display_text_range": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                },
                "entities": {
                    "$ref": "#/definitions/FluffyEntities"
                },
                "favorite_count": {
                    "type": "integer"
                },
                "favorited": {
                    "type": "boolean"
                },
                "full_text": {
                    "type": "string"
                },
                "in_reply_to_screen_name": {
                    "type": "string"
                },
                "in_reply_to_status_id_str": {
                    "type": "string"
                },
                "in_reply_to_user_id_str": {
                    "type": "string",
                    "format": "integer"
                },
                "is_quote_status": {
                    "type": "boolean"
                },
                "lang": {
                    "type": "string"
                },
                "possibly_sensitive": {
                    "type": "boolean"
                },
                "possibly_sensitive_editable": {
                    "type": "boolean"
                },
                "quote_count": {
                    "type": "integer"
                },
                "quoted_status_id_str": {
                    "type": "string"
                },
                "quoted_status_permalink": {
                    "$ref": "#/definitions/QuotedStatusPermalink"
                },
                "reply_count": {
                    "type": "integer"
                },
                "retweet_count": {
                    "type": "integer"
                },
                "retweeted": {
                    "type": "boolean"
                },
                "user_id_str": {
                    "type": "string",
                    "format": "integer"
                },
                "id_str": {
                    "type": "string"
                },
                "self_thread": {
                    "$ref": "#/definitions/SelfThread"
                }
            },
            "required": [],
            "title": "FluffyLegacy"
        },
        "FluffyEntities": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "user_mentions": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/UserMention"
                    }
                },
                "urls": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/URL"
                    }
                },
                "hashtags": {
                    "type": "array",
                    "items": {}
                },
                "symbols": {
                    "type": "array",
                    "items": {}
                }
            },
            "required": [],
            "title": "FluffyEntities"
        },
        "UserMention": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "id_str": {
                    "type": "string",
                    "format": "integer"
                },
                "name": {
                    "type": "string"
                },
                "screen_name": {
                    "type": "string"
                },
                "indices": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    }
                }
            },
            "required": [],
            "title": "UserMention"
        },
        "QuotedStatusPermalink": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "url": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                },
                "expanded": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                },
                "display": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "QuotedStatusPermalink"
        },
        "SelfThread": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "id_str": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "SelfThread"
        },
        "QuickPromoteEligibility": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "eligibility": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "QuickPromoteEligibility"
        },
        "QuotedStatusResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "result": {
                    "$ref": "#/definitions/QuotedStatusResultResult"
                }
            },
            "required": [],
            "title": "QuotedStatusResult"
        },
        "QuotedStatusResultResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "__typename": {
                    "type": "string"
                },
                "rest_id": {
                    "type": "string"
                },
                "has_birdwatch_notes": {
                    "type": "boolean"
                },
                "core": {
                    "$ref": "#/definitions/FluffyCore"
                },
                "edit_control": {
                    "$ref": "#/definitions/EditControl"
                },
                "is_translatable": {
                    "type": "boolean"
                },
                "views": {
                    "$ref": "#/definitions/Views"
                },
                "source": {
                    "type": "string"
                },
                "quotedRefResult": {
                    "$ref": "#/definitions/QuotedRefResult"
                },
                "legacy": {
                    "$ref": "#/definitions/FluffyLegacy"
                }
            },
            "required": [],
            "title": "QuotedStatusResultResult"
        },
        "FluffyCore": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "user_results": {
                    "$ref": "#/definitions/FluffyUserResults"
                }
            },
            "required": [],
            "title": "FluffyCore"
        },
        "FluffyUserResults": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "result": {
                    "$ref": "#/definitions/FluffyResult"
                }
            },
            "required": [],
            "title": "FluffyUserResults"
        },
        "FluffyResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "__typename": {
                    "type": "string"
                },
                "id": {
                    "type": "string"
                },
                "rest_id": {
                    "type": "string",
                    "format": "integer"
                },
                "affiliates_highlighted_label": {
                    "$ref": "#/definitions/AffiliatesHighlightedLabel"
                },
                "is_blue_verified": {
                    "type": "boolean"
                },
                "profile_image_shape": {
                    "type": "string"
                },
                "legacy": {
                    "$ref": "#/definitions/PurpleLegacy"
                },
                "professional": {
                    "$ref": "#/definitions/Professional"
                }
            },
            "required": [],
            "title": "FluffyResult"
        },
        "Professional": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "rest_id": {
                    "type": "string"
                },
                "professional_type": {
                    "type": "string"
                },
                "category": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Category"
                    }
                }
            },
            "required": [],
            "title": "Professional"
        },
        "Category": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "icon_name": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "Category"
        },
        "QuotedRefResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "result": {
                    "$ref": "#/definitions/QuotedRefResultResult"
                }
            },
            "required": [],
            "title": "QuotedRefResult"
        },
        "QuotedRefResultResult": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "__typename": {
                    "type": "string"
                },
                "rest_id": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "QuotedRefResultResult"
        },
        "Views": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "count": {
                    "type": "string",
                    "format": "integer"
                },
                "state": {
                    "type": "string"
                }
            },
            "required": [],
            "title": "Views"
        }
    }
}"""
}
}

def traverse_path(path:str) -> List[str]:
    path_components = [component for component in path.split("/") if component not in ["","."]]
    curr_fs = fs
    for component in path_components:
        if component not in curr_fs:
            return f"Error: unknown path {path}."
        curr_fs = curr_fs[component]
    return curr_fs

def ls(path:str) -> List[str]:
    """
    Lists the files in a directory.
    """
    print("calling ls",path)
    curr_fs = traverse_path(path)
    if type(curr_fs)==dict:
        return list(curr_fs.keys())
    else:
        return f"Error: {path} is a file, not a directory."
    
def cat(path:str) -> str:
    """
    Prints the contents of a file.
    """
    print("calling cat",path)
    curr_fs = traverse_path(path)
    if type(curr_fs)==str:
        return curr_fs
    else:
        return f"Error: {path} is a directory, not a file."

def write_to_file(path:str,contents:str) -> str:
    """
    Writes to a file.
    """
    path_components = [component for component in path.split("/") if component not in ["","."]]
    if len(path_components)==0:
        return f"Error: {path} is not a valid path."
    filename = path_components[-1]
    path_components = path_components[:-1]
    curr_fs = traverse_path("/".join(path_components))
    if type(curr_fs)==str:
        return f"Error: {path} is a file, not a directory."
    curr_fs[filename] = contents
    return f"Successfully wrote to {path}."

def ask_clarifying_question(question:str):
    """
    Asks the user a clarifying question about the objective.
    Use this function sparingly!
    """
    return input("Question from the model: "+question)

def add_to_my_notebook(note:str):
    """
    Adds a note to your notebook. This is good for remembering important info.
    """
    global notebook
    if len(notebook) + len(note) > 4000:
        return "Your notebook is full! You should rewrite it to make it shorter."
    notebook += "\n"+note
    return "Added to notebook."

def rewrite_my_notebook(note:str):
    """
    Replaces your notebook with a new note.
    """
    if len(note) > 4000:
        return "This note is too long! Try writing a shorter one."
    global notebook
    notebook = note
    return "Replaced notebook."

def delegate_to_babyagi(sub_objective:str):
    """
    Spawns a new BabyAGI to help you out.
    You can give it an objective too!
    Some usecases: make BabyAGI download a big webpage for you, or summarize a long document.
    Recommendation: tell BabyAGI save its results into a file!
    """
    print("Delegated to babyagi. This is not implemented yet!")

import os
api_key = os.environ['OPENAI_API_KEY']

functions = [ls,cat,add_to_my_notebook,rewrite_my_notebook,write_to_file]
convo = ChatConversation(system=system)
convo.messages.append({
    "role":"user",
    "content":user(),
})

print("\n"*10,"Starting","\n"*10)

while True:
    print("-" * 50 + "Running new iter" + "-" * 50)
    completion = convo.generate(functions=functions)
    print(completion)
    resp = input("Press enter to continue. Press q to quit.")
    if resp == "q":
        break
    else:
        convo.messages.append({
            "role":"user",
            "content":resp,
        })

print(fs.get("README.md","No README.md found."))
print(f"Done. Saved in folder {convo.id}.")