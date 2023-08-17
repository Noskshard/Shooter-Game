def enemy_vel_based_on_level(default_enemy_vel, level, enemy):
    vel = default_enemy_vel
    scaling = 0.1
    if enemy.color == "blue":
        vel = 1.5 * vel + scaling * level
    elif enemy.color == "red":
        vel = (vel + scaling * level) /2
    elif enemy.color == "green":
        vel = vel - scaling * level
    return vel

def enemy_collision_damage(enemy, default_damage):
    if enemy.color == "blue":
        return default_damage / 2
    elif enemy.color == "red":
        return default_damage * 2
    return default_damage