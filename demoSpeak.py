from Avatar import Avatar

p = Avatar()

response = p.listen("testing testing", False, False)

p.say(f"You said {response} the first time")
p.say(f"You said {response}", False)