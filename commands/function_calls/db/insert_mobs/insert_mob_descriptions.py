import sqlite3

try:
    sqliteConnection = sqlite3.connect('mobspawn.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('frenzy boar', '```Off In the distance {character_name} hears a sound cue as a medium sized {spawns} with blue fur, glowing red eyes, a flat snout and sharp tusks protruding from both sides of its mouth appears at your forefront.```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('dire wolf', '```A dire wolf!```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('large nepenthes', '```{character_name} sees as a massive glowing aura rise from the ground as  {random_monster_spawn} {spawns} has appeared!  This dangerous creature has a red fruit attached to its head, which, if damaged, will emit an odor that will attract other Little Nepenthes to your location. Low-level players should be especially cautious when encountering the Large Nepenthes, as it can be almost guaranteed death to engage with it without careful planning. Use caution when attacking this creature to avoid damaging the fruit and attracting additional enemies. The first two consisted of the monster using its dagger-like vine leaves to either swipe or lunge at its target. The monster also possessed a special corrosive spray attack that could reach targets up to five meters away. The corrosive spray dealt substantial damage both to a players hit points, as well as impeded the unlucky players movement due to the stickiness of the liquid it expelled. However, the sprays area of effect was limited to thirty degrees in front of the plant. Since the monster signaled its spray attacks with a clearcut pre-motion, consisting of the monster puffing its pitcher, it was relatively easy for a player to jump out of the way if they timed their moves right. On the other hand, since Little Nepenthes were primarily specialized for the offensive, they tend to have weak defense against player attacks on them ```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('little nepenthes', '```{character_name} notices an aura rising from the ground as  {random_monster_spawn} {spawns} has appeared!  Despite being called Little Nepenthes, there was nothing little about this predatory plant as it was a meter and a half tall. Its lower body consisted mostly of countless roots that were used to move around. It had two arm-like vines with pointed leaves attached to either side of its body, just above the roots. The center of its head held a wide red mouth with viscous liquids dribbling out of it as it opened and closed. The first two consisted of the monster using its dagger-like vine leaves to either swipe or lunge at its target. The monster also possessed a special corrosive spray attack that could reach targets up to five meters away. The corrosive spray dealt substantial damage both to a players hit points and their gears durability, as well as impeded the unlucky players movement due to the stickiness of the liquid it expelled. However, the sprays area of effect was limited to thirty degrees in front of the plant. Since the monster signaled its spray attacks with a clearcut pre-motion, consisting of the monster puffing its pitcher, it was relatively easy for a player to jump out of the way if they timed their moves right. On the other hand, since Little Nepenthes were primarily specialized for the offensive, they had weak defense against player attacks on them.```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('white tailed buck', '```{character_name} notices a stream of water that follows a wooded area up ahead. After further investigation, {random_monster_spawn} {spawns} can be seen drinking from the stream. its reddish brown coat blending in with the foliage of the Eastern Plains. Its most distinctive feature is the white underside of its tail, which stands out against the darker fur of its body. You can see the powerful muscles of its hind legs, a clear indication of its ability to deliver strong kicks. As it turns its head to look at you, you cant help but feel a sense of danger emanating from its razor sharp antlers. These antlers have a 10% chance to cause bleeding damage on impact, so its best to be cautious.```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('goat', '```{character_name} walks along the base of the Eastern Mountains before being alerted by a sound cue of a mob spawn to their left. {random_monster_spawn} {spawns} has a thick, coarse coat of fur that ranges in color from white to gray, with black markings on its face and legs. Its horns are long and curved, and it has a sturdy build. Its horns have a 10% chance to cause a bleeding status. ```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('skeleton gladiator', '```As {character_name} makes their way through the winding corridors of the first floor dungeon, you can hear the sound of clashing metal and the grunts of exertion up ahead. You cautiously approach, your hand on your weapon, ready to defend yourself at a moments notice. Suddenly, {random_monster_spawn} {spawns} emerges from the shadows, its bony fingers grasping a wicked-looking sword. Its empty eye sockets seem to bore into your soul as it snarls at you, revealing a mouthful of sharp teeth. a formidable opponent known for its brutal combat skills and relentless attacks. Its bronze med helmet and wooden shield mark it as a seasoned warrior, and you know you will have to fight with all your might to emerge victorious. ```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('giant spider', '```As {character_name} ventures deeper into the first floor dungeon,a faint rustling sound comes from ahead. {random_monster_spawn} {spawns} its multiple legs scrabbling on the stone floor. Its bulbous abdomen and multiple eyes give it an unsettling, otherworldly appearance. Known for its venomous fangs and deadly attacks. Standing roughly one meter tall, this spider poses a serious threat to anyone who dares to challenge it. ```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('goblin', '```As {character_name} delve deeper into the first floor dungeon, a faint chattering sound can be heard coming from ahead. A very distinct sound fills the entire dungeon that only an SAO player could identify as {random_monster_spawn} {spawns} spawn down the way as small, green-skinned figure(s) begin taking strides towards the player(s), its beady eyes fixed on what they see as prey. It bares its sharp teeth and brandishes a crude weapon before fully charging for battle.```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('bat', '```As {character_name} navigates through the floor one dungeon, A flapping sound can be heard coming from above. The player(s) look up, but see nothing but darkness. In that same instance, {random_monster_spawn} {spawns} The bat(s) descends upon you, wings beating frantically as the bats(s) dive towards you. They are known for being incredibly agile and precise in their strikes, narrowly avoiding your initial attempts to fend them off. ```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('mountain troll', '```{character_name} continues wandering through the Floor One dungeon upon feeling an odd sensation beneath their feet. Almost as if something was rushing towards them. {random_monster_spawn} {spawns} Its hard exoskeleton provides significant defense against attacks. This creature is known for its powerful burrowing ability and can surprise players by bursting out of the ground with incredible speed and power. ```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('scavenger toad', '```{character_name} makes their way through the Eastern Forest before a burst of energy begins to materialize. {random_monster_spawn}{spawns}.  Known to be  large, green, slimy creatures with two glowing red eyes on either side of its head. It has two short horns protruding from the top of its head and red markings on its back, head, and front legs. They can maneuver themselves quickly by making large leaps across any form of battlefield. Scavenger Toads have a 15% chance to secrete a poison status effect due to them producing it through their skin.```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    sqlite_insert_query = """INSERT INTO mob_descriptions
                          (name, mob_description)
                           VALUES 
                          ('cow', '```{character_name} makes their way through the Eastern Plains before a bright light appears in the field filled with tall grass and wildflowers. A thick bell dong can be heard as the light vanishes. {random_monster_spawn} {spawns}.  The player(s) realize this isnt any normal cow. The normal creamy white coat is now armored, bolstering its defenses, and it seems to have a set of sharp, metallic horns. You draw your weapon, prepared for a fight, as the cow charges at you with a fierce determination.```')"""

    count = cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()

    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")
