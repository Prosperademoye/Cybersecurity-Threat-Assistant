training_data = [] # this array is to hold formatted training data suitable for Spacy
    # for text, entities in zip(data, labels): #Zip the data and labels so we can loop through both of them at the same time. This loop is done because spacy need the labels in a specific format
    #     ents = []
    #     for entity in entities: #loop through labels
    #         start = entity[0] # start is the first number in the tuple
    #         end = entity[1] 
    #         label = entity[2]
    #         ents.append((start, end, label))
    #     training_data.append((text, {"entities": ents})) # Spacy need the labels in this format 
    # #So instead of [(12, 20, "MALWARE") we have ("This is a sample text about malware.", {"entities": [(25, 32, "MALWARE")]}). The latter is the format spacy expects