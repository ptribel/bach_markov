#!/usr/bin/env python
# coding: utf-8

# # Markov Generator from Bach Inventions

# In[1]:


from mido import MidiFile, Message, MidiTrack
import numpy as np
import matplotlib.pyplot as plt
import itertools
LEVELS = 4
LENGTH = 60

# We extract all the note beginnings and store it in a numpy array `tracks`.

# In[2]:


tracks = []
for i in range(1, 16):
    input_file = MidiFile(str(i) + '.mid')
    for track in input_file.tracks[1:]:
        t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
        tracks.append(t)
        
for i in range(787, 802):
    input_file = MidiFile('bwv' + str(i) + '.mid')
    for track in input_file.tracks[1:]:
        t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
        tracks.append(t)

"""for i in range(806, 818):
    input_file = MidiFile('bwv' + str(i) + '.mid')
    for track in input_file.tracks[1:]:
        t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
        tracks.append(t)
        
for i in range(825, 831):
    input_file = MidiFile('bwv' + str(i) + '.mid')
    for track in input_file.tracks[1:]:
        t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
        tracks.append(t)

for i in range(832, 834):
    input_file = MidiFile('bwv' + str(i) + '.mid')
    for track in input_file.tracks[1:]:
        t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
        tracks.append(t)
        """
input_file = MidiFile('goldberg.mid')
for track in input_file.tracks[1:]:
    t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
    tracks.append(t)
    
input_file = MidiFile('toccata.mid')
for track in input_file.tracks[1:]:
    t = np.array([int(i.note) for i in track[1:] if i.type=='note_on' and i.velocity>0])
    tracks.append(t)


# In[3]:


tracks = np.concatenate(tracks)


# Now tracks contains 17594 notes. We ignore the side effects at the end of each track.

# In[4]:


print(len(tracks), " notes read")


# Let us store the probability for each note to be followed by another one. The highest note reached in Bach's invention is

# In[5]:


max_note = int(max(tracks))
min_note = int(min(tracks))

# Therefore we build a 2-dimensional matrix of $85\times85$, and we compute the probability that one note follows another. This gives a Markov matrix of memory $1$.

# In[ ]:


def get_markov(level):
    res = {}
    for group in range(len(tracks)-level):
        key = tuple(tracks[group:group+level])
        if key not in res.keys():
            res[key] = np.zeros(max_note+1)
        res[key][int(tracks[group+level])] += 1
    for group in range(len(tracks)-level):
        key = tuple(tracks[group:group+level])
        res[key] /= np.sum(res[key])
    return res

print("Preparing matrix...")
markov = get_markov(LEVELS)
print("Done !") 

# In[ ]:

#markov[tuple([i for i in tracks[:LEVELS]])]


# As an example, the following plot gives the statistical distribution of all the notes following notes $60$ and $60$ in a group.

# In[ ]:


#plt.plot(markov[tuple([i for i in tracks[:LEVELS]])])


# Let us now build a method that, given a certain group, outputs a random note according to the previously computed distributions.

# In[ ]:


def output_note(input_group):
    if input_group in markov.keys():
        return np.random.choice(list(range(max_note+1)), p=markov[input_group])
    else:
        return np.random.choice(list(range(min_note, max_note)))


# Let us now build a method that, given a first group, outputs a line of different notes (forming a melody).

# In[ ]:


def output_melody(input_group, length, level):
    res = list(input_group)
    for _ in range(length):
        res.append(output_note(tuple(res[-level:])))
    return res


# In[ ]:


melody = output_melody(tuple([int(i) for i in tracks[:LEVELS]]), LENGTH, LEVELS)
print(melody)

# Let us now convert this melody to a midi file:

# In[ ]:


def convert_to_midi(melody, filename):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    t = 500
    for i in melody:
        track.append(Message('note_on', note=i, time=0))
        track.append(Message('note_off', note=i, time=300))
    mid.save(filename)
convert_to_midi(melody, 'test.mid')


# In[ ]:




