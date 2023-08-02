def check_beast_beastdb():
    return """SELECT 
                base_level, base_hp, base_str, base_def, base_spd, base_dex, 
                hp_growth_rate, str_growth_rate, def_growth_rate, spd_growth_rate, dex_growth_rate 
                FROM 
                    beastdb 
                    WHERE 
                        beasts_name = ?;"""

def add_beast_characters_beasts():
    return """INSERT INTO 
                    characters_beasts
                        (pet_name, pet_nickname, level, hp, str, 
                        def, spd, dex, uv_hp, uv_str, uv_def, 
                        uv_spd, uv_dex, players_tag, unique_identifier) 
                        VALUES 
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""

def check_beast_characters_beasts():
    return """SELECT 
                pet_name, pet_nickname, level, hp, str, 
                def, spd, dex 
                FROM 
                    characters_beasts
                    WHERE 
                        pet_nickname = ? 
                        AND players_tag = ?
                        """

def compare_beast_stats_characters_beasts():
    return """SELECT 
                    characters_beasts.level, characters_beasts.hp, characters_beasts.str, 
                    characters_beasts.def, characters_beasts.spd, characters_beasts.dex, 
                    beastdb.hp_growth_rate, beastdb.str_growth_rate, 
                    beastdb.def_growth_rate, beastdb.spd_growth_rate,
                    beastdb.dex_growth_rate, beastdb.base_hp, 
                    beastdb.base_str, beastdb.base_def, 
                    beastdb.base_spd, beastdb.base_dex 
                    FROM 
                        characters_beasts INNER JOIN beastdb 
                        ON 
                            characters_beasts.pet_name = beastdb.beasts_name 
                            WHERE                            
                                    pet_nickname = ?"""

def level_up_and_down_beast_characters_beasts():
    return """UPDATE 
                    characters_beasts 
                    SET 
                        level = ?, hp = ?, str = ?, def = ?, spd = ?, dex = ?
                        WHERE 
                            players_tag = ? 
                            AND 
                                pet_nickname = ?"""

def get_players_stats_characters():
    return """SELECT 
                str, def, spd, dex, cha 
                FROM 
                    charactersheets WHERE nickname = ?;"""

def get_all_player_fields_characters():
    return """SELECT 
                firstName, lastName, height, size, age, skillList, 
                inventory, bio, guild, class, playerColor, birthday, nickname, 
                uniqueSkills, proficiencySkills, currentWeaponEquipped, col, 
                experience, level, str, def, spd, playerStatus, party_id 
                FROM 
                    charactersheets 
                    WHERE 
                        nickname =  ?"""

def add_to_guild_characters():
    return """UPDATE 
                charactersheets 
                SET 
                    guild =  ? 
                    WHERE 
                        nickname = ?;"""
                        
def get_guild_characters():
    return """SELECT guild_name FROM guilds WHERE guild_name = '" + guild_name_lower ;"""

def get_guild_approvers_characters():
    return """SELECT guild_approvers FROM guilds WHERE guild_name = ?;"""

def get_player_characters():
    return """SELECT 
                nickname 
                FROM 
                    charactersheets 
                    WHERE 
                        nickname = ?; """
def check_item_exists_equipment():
    return """SELECT 
                weapon_name
                FROM
                    weapons
                    WHERE
                        weapon_name = ?
                UNION
                SELECT
                    armor_name
                    FROM
                        armor
                        WHERE
                            armor_name = ?
                UNION
                SELECT
                    name
                    FROM
                        fishdb
                        WHERE
                            name = ?                              
                UNION
                SELECT
                    item
                    FROM   
                        items
                        WHERE
                            item = ?
                UNION
                SELECT
                    name
                    FROM
                        blacksmithing_materials
                        WHERE
                            name = ?;"""

def check_item_equipment():
    return """SELECT
                item, item_description, rarity, droppedby 
                FROM   
                    items
                    WHERE
                        item = ?;"""

def check_armor_equipment():
    return """SELECT
                armor_name, armor_description, 
                armor_rarity, how_to_obtain, base_defense, 
                additional_effects, armor_material, catagory 
                FROM   
                    armor
                    WHERE
                        armor_name = ?;"""

def check_weapon_equipment():
    return """SELECT
                weapon_name, weapon_description, 
                weapon_rarity, how_to_obtain, base_power,
                additional_effects, crit_chance, weapon_material,
                weapon_attack_type, catagory 
                FROM   
                    weapons
                    WHERE
                        weapon_name = ?;"""

def check_fish_equipment():
    return """SELECT
                name, description, rarity, how_to_obtain,
                location, difficulty 
                FROM   
                    fishdb
                    WHERE
                        name = ?;"""

def check_blacksmithing_material_equipment():
    return """SELECT
                name, description, rarity, how_to_obtain,
                location, difficulty, processing_type, processed_into, catagory 
                FROM   
                    blacksmithing_materials
                    WHERE
                        name = ?;"""

def add_blacksmithing_material_to_server_equipment():
    return """INSERT INTO 
                                blacksmithing_materials
                                        (name, description, 
                                        rarity, how_to_obtain, 
                                        location, difficulty, 
                                        processing_type, processed_into, catagory) 
                                        VALUES 
                                                (?,?,?,?,?,?,?,?,?);"""   

def remove_blacksmithing_material_from_server_equipment():
    return """DELETE 
        FROM 
        blacksmithing_materials 
                WHERE 
                        material_name = ?;"""

def invite_valid_sessions():
    return """SELECT invite_id, expired
        FROM 
        invites 
                WHERE 
                    invite_id = ?;"""

def remove_invite_sessions():
    return """DELETE
        FROM
            invites
            WHERE
                invite_id = ?"""

def get_party_id_charactersheets():
    return """SELECT party_id 
        FROM 
        charactersheets 
                WHERE 
                        nickname = ?;"""

def add_party_charactersheets():
    return """UPDATE charactersheets 
        SET 
            party_id = ? 
                WHERE 
                        nickname = ?
                        AND
                            discord_tag = ?;"""

def add_party_sessions():
    return """INSERT
        INTO
            party(party_id, party_members, party_name, party_count)
            VALUES 
                (?,?,?,?);"""

def update_party_sessions():
    return """UPDATE party
            SET 
                party_count = ?,
                party_members = ?
                    WHERE
                        party_id = ?;
                """
                

def remove_party_charactersheets():
    return """UPDATE charactersheets
            SET 
                party_id = ""
                WHERE
                    nickname = ?;
                """
                
def update_all_players_in_party_charactersheet(usernames):
    return """UPDATE charactersheets
                SET 
                    party_id = ?
                    WHERE 
                        nickname IN ({})""".format(", ".join(["?" for _ in usernames]))

                
def get_party_information():
    return """SELECT party_members, party_count, party_id
        FROM 
            party
            WHERE 
                party_id = ?;"""

def invite_sessions():
    return """INSERT INTO
                invites (invite_id, inviter, invitee, party_id, expired)
                VALUES
                    (?,?,?,?,?);
                    """

def remove_party_invite():
    return """DELETE
            FROM
                invites
                WHERE
                    invite_id = ?;"""
                    
def remove_party_sessions():
    return """DELETE
            FROM
                party
                WHERE
                    party_id = ?;"""