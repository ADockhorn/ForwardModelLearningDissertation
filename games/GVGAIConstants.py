def get_images(game):
    if game == "butterflies":
        return {" ": ['sprites/oryx/grass_15.png'],  # empty
                "w": ['sprites/oryx/grass_15.png', 'sprites/oryx/tree2.png'],
                "b": ['sprites/oryx/grass_15.png', 'sprites/newset/butterfly1.png'],
                "x": ['sprites/oryx/grass_15.png', 'sprites/newset/butterfly1.png'],
                "a": ['sprites/oryx/grass_15.png', 'sprites/oryx/angel1.png'],
                "c": ['sprites/oryx/grass_15.png', 'sprites/newset/cocoonb2.png']}
    if game == 'bait':
        return {'a': ['sprites/oryx/backLBrown.png'],
                'b': ['sprites/oryx/backLBrown.png', 'sprites/oryx/swordman1_0.png'],
                'c': ['sprites/oryx/backLBrown.png', 'sprites/oryx/doorclosed1.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/oryx/swordman1_0.png', 'sprites/newset/hole1.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/newset/block3.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/newset/hole1.png'],
                'h': ['sprites/oryx/backLBrown.png', 'sprites/oryx/mushroom2.png'],
                'i': ['sprites/oryx/backLBrown.png', 'sprites/oryx/key2.png', 'sprites/newset/block3.png'],
                'j': ['sprites/oryx/backLBrown.png', 'sprites/oryx/key2.png']}
    if game == 'bait':
        return {'a': ['sprites/oryx/backLBrown.png', 'sprites/oryx/swordman1_0.png'],
                'b': ['sprites/oryx/backLBrown.png', 'sprites/oryx/doorclosed1.png'],
                'c': ['sprites/oryx/backLBrown.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/oryx/key2.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/oryx/swordman1_0.png', 'sprites/newset/hole1.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/oryx/swordmankey1_0.png'],
                'h': ['sprites/oryx/backLBrown.png', 'sprites/newset/block3.png'],
                'i': ['sprites/oryx/backLBrown.png', 'sprites/oryx/mushroom2.png'],
                'j': ['sprites/oryx/backLBrown.png', 'sprites/newset/hole1.png']}

    if game == 'brainman':
        return {'a': ['sprites/newset/floor2.png'], 'b': ['sprites/newset/floor2.png', 'sprites/oryx/diamond3.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/key3.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/prince1.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/diamond1.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/newset/block3.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/newset/exit2.png'],
                'i': ['sprites/newset/floor2.png', 'sprites/oryx/diamond2.png'],
                'j': ['sprites/newset/floor2.png', 'sprites/oryx/doorclosed1.png'],
                'k': ['sprites/newset/floor2.png', 'sprites/oryx/key3.png']}

    if game == 'catapults':
        return {'a': ['sprites/oryx/grass_15.png'],
                'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/bookRight.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png'],
                'd': ['sprites/oryx/grass_15.png'], 'e': ['sprites/oryx/grass_15.png', 'sprites/oryx/bush5.png'],
                'f': ['sprites/oryx/grass_15.png', 'sprites/oryx/bookUp.png'],
                'g': ['sprites/oryx/grass_15.png', 'sprites/oryx/bookDown.png'],
                'h': ['sprites/oryx/grass_15.png', 'sprites/oryx/vampire1.png'],
                'i': ['sprites/oryx/grass_15.png', 'sprites/oryx/seaWater.png'],
                'j': ['sprites/oryx/grass_15.png', 'sprites/oryx/vampire1.png', 'sprites/oryx/seaWater.png'],
                'k': ['sprites/oryx/grass_15.png', 'sprites/oryx/bookLeft.png'],
                'l': ['sprites/oryx/grass_15.png', 'sprites/oryx/seaWater.png']}

    if game == 'cec2':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/cspell1.png', 'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/necromancer1.png', 'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/necromancer1.png', 'sprites/oryx/cspell2.png',
                      'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/staff2.png', 'sprites/oryx/necromancer1.png',
                      'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/necromancer1.png', 'sprites/oryx/cspell1.png',
                      'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/oryx/staff2.png', 'sprites/newset/floor2.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/oryx/cspell2.png', 'sprites/newset/floor2.png'],
                'i': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/oryx/staff2.png'],
                'j': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png']}

    if game == 'cec3':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png', 'sprites/newset/block1.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/newset/floor3.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/cspell4.png', 'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png']}

    if game == 'chainreaction':
        return {'a': ['sprites/oryx/backLBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'b': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png'],
                'c': ['sprites/oryx/backLBrown.png', 'sprites/oryx/yeti2.png', 'sprites/oryx/backLBrown.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/oryx/yeti2.png', 'sprites/oryx/backLBrown.png'],
                'h': ['sprites/oryx/backLBrown.png', 'sprites/oryx/yeti2.png', 'sprites/oryx/backLBrown.png',
                      'sprites/newset/hole1.png'],
                'i': ['sprites/oryx/backLBrown.png', 'sprites/oryx/yeti2.png', 'sprites/oryx/backLBrown.png'],
                'j': ['sprites/oryx/backLBrown.png', 'sprites/oryx/yeti2.png', 'sprites/oryx/backLBrown.png',
                      'sprites/newset/exit2.png'],
                'k': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png', 'sprites/newset/block2.png'],
                'l': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png', 'sprites/newset/exit2.png'],
                'm': ['sprites/oryx/backLBrown.png', 'sprites/oryx/backLBrown.png', 'sprites/newset/hole1.png']}

    if game == 'chase':
        return {'a': ['sprites/oryx/grass_15.png'],
                'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png', 'sprites/oryx/bird1.png',
                      'sprites/oryx/bird1.png', 'sprites/oryx/bird1.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png', 'sprites/oryx/bird3.png'],
                'd': ['sprites/oryx/grass_15.png', 'sprites/oryx/tree2.png'],
                'e': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png'],
                'f': ['sprites/oryx/grass_15.png', 'sprites/oryx/worm2.png'],
                'g': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png'],
                'h': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird3.png'],
                'i': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png', 'sprites/oryx/bird1.png'],
                'j': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png', 'sprites/oryx/bird1.png',
                      'sprites/oryx/bird1.png'],
                'k': ['sprites/oryx/grass_15.png', 'sprites/oryx/worm2.png', 'sprites/oryx/princess1.png']}

    if game == 'chipschallenge':
        return {'a': ['sprites/oryx/floor3.png'], 'b': ['sprites/oryx/floor3.png', 'sprites/oryx/potion4.png'],
                'c': ['sprites/oryx/floor3.png', 'sprites/oryx/slime3.png'],
                'd': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png'],
                'e': ['sprites/oryx/floor3.png', 'sprites/oryx/doorclosed1.png'],
                'f': ['sprites/oryx/floor3.png', 'sprites/newset/block3.png'],
                'g': ['sprites/oryx/floor3.png', 'sprites/oryx/potion1.png'],
                'h': ['sprites/oryx/floor3.png', 'sprites/oryx/rogue.png'],
                'i': ['sprites/oryx/floor3.png', 'sprites/oryx/boots3.png'],
                'j': ['sprites/oryx/floor3.png', 'sprites/oryx/gold1.png'],
                'k': ['sprites/oryx/floor3.png', 'sprites/oryx/slime6.png'],
                'l': ['sprites/oryx/floor3.png', 'sprites/oryx/fire1.png'],
                'm': ['sprites/oryx/floor3.png', 'sprites/oryx/boots2.png'],
                'n': ['sprites/oryx/floor3.png', 'sprites/newset/exit2.png'],
                'o': ['sprites/oryx/floor3.png', 'sprites/oryx/potion5.png'],
                'p': ['sprites/oryx/floor3.png', 'sprites/oryx/rogue.png', 'sprites/oryx/fire1.png'],
                'q': ['sprites/oryx/floor3.png', 'sprites/newset/water.png'],
                'r': ['sprites/oryx/floor3.png', 'sprites/oryx/slime2.png'],
                's': ['sprites/oryx/floor3.png', 'sprites/oryx/slime1.png'],
                't': ['sprites/oryx/floor3.png', 'sprites/oryx/rogue.png', 'sprites/newset/water.png'],
                'u': ['sprites/oryx/floor3.png', 'sprites/oryx/potion3.png']}

    if game == 'clusters':
        return {'a': ['sprites/oryx/floor3.png'], 'b': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png'],
                'c': ['sprites/oryx/floor3.png', 'sprites/newset/blockG.png'],
                'd': ['sprites/oryx/floor3.png', 'sprites/oryx/knight1.png'],
                'e': ['sprites/oryx/floor3.png', 'sprites/newset/blockR.png'],
                'f': ['sprites/oryx/floor3.png', 'sprites/newset/blockR2.png'],
                'g': ['sprites/oryx/floor3.png', 'sprites/oryx/spike2.png'],
                'h': ['sprites/oryx/floor3.png', 'sprites/oryx/spike2.png', 'sprites/oryx/knight1.png'],
                'i': ['sprites/oryx/floor3.png', 'sprites/newset/blockG2.png'],
                'j': ['sprites/oryx/floor3.png', 'sprites/newset/blockB.png'],
                'k': ['sprites/oryx/floor3.png', 'sprites/newset/blockB2.png']}

    if game == 'colourescape':
        return {'a': ['sprites/oryx/floor3.png'], 'b': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png'],
                'c': ['sprites/oryx/floor3.png', 'sprites/newset/tile1.png', 'sprites/newset/girl2.png'],
                'd': ['sprites/oryx/floor3.png', 'sprites/newset/block2.png'],
                'e': ['sprites/oryx/floor3.png', 'sprites/newset/blockR.png'],
                'f': ['sprites/oryx/floor3.png', 'sprites/newset/girl2.png'],
                'g': ['sprites/oryx/floor3.png', 'sprites/newset/girl5.png'],
                'h': ['sprites/oryx/floor3.png', 'sprites/oryx/spike2.png', 'sprites/newset/girl2.png'],
                'i': ['sprites/oryx/floor3.png', 'sprites/oryx/spike2.png'],
                'j': ['sprites/oryx/floor3.png', 'sprites/oryx/doorclosed1.png'],
                'k': ['sprites/oryx/floor3.png', 'sprites/oryx/spike2.png', 'sprites/newset/girl5.png'],
                'l': ['sprites/oryx/floor3.png', 'sprites/newset/tile1.png'],
                'm': ['sprites/oryx/floor3.png', 'sprites/newset/girl3.png'],
                'n': ['sprites/oryx/floor3.png', 'sprites/newset/tile3.png'],
                'o': ['sprites/oryx/floor3.png', 'sprites/oryx/spike2.png', 'sprites/newset/girl1.png'],
                'p': ['sprites/oryx/floor3.png', 'sprites/newset/blockG.png'],
                'q': ['sprites/oryx/floor3.png', 'sprites/newset/tile4.png', 'sprites/newset/girl1.png'],
                'r': ['sprites/oryx/floor3.png', 'sprites/newset/tile3.png', 'sprites/newset/girl5.png'],
                's': ['sprites/oryx/floor3.png', 'sprites/newset/floor6.png'],
                't': ['sprites/oryx/floor3.png', 'sprites/newset/tile4.png'],
                'u': ['sprites/oryx/floor3.png', 'sprites/newset/girl1.png'],
                'v': ['sprites/oryx/floor3.png', 'sprites/newset/blockB.png']}

    if game == 'cookmepasta':
        return {'a': ['sprites/newset/floor6.png'], 'b': ['sprites/newset/floor6.png', 'sprites/newset/floor4.png'],
                'c': ['sprites/newset/floor6.png', 'sprites/oryx/key2.png'],
                'd': ['sprites/newset/floor6.png', 'sprites/newset/tuna.png'],
                'e': ['sprites/newset/floor6.png', 'sprites/newset/chef.png'],
                'f': ['sprites/newset/floor6.png', 'sprites/newset/lock1.png'],
                'g': ['sprites/newset/floor6.png', 'sprites/newset/tomato.png'],
                'h': ['sprites/newset/floor6.png', 'sprites/newset/boilingwater.png'],
                'i': ['sprites/newset/floor6.png', 'sprites/newset/pasta.png']}

    if game == 'decepticoins':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/piranha1.png',
                      'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/newset/piranha1.png', 'sprites/newset/piranha1.png',
                      'sprites/newset/piranha1.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/newset/floor3.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/newset/piranha1.png', 'sprites/newset/piranha1.png',
                      'sprites/newset/floor2.png'], 'h': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'i': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/oryx/cspell4.png',
                      'sprites/newset/floor2.png'],
                'j': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png', 'sprites/newset/block1.png'],
                'k': ['sprites/newset/floor2.png', 'sprites/newset/piranha1.png', 'sprites/newset/floor2.png'],
                'l': ['sprites/newset/floor2.png', 'sprites/oryx/cspell4.png', 'sprites/newset/floor2.png'],
                'm': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/piranha1.png',
                      'sprites/newset/floor2.png'],
                'n': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/piranha1.png',
                      'sprites/newset/piranha1.png', 'sprites/newset/floor2.png']}

    if game == 'deceptizelda':
        return {'a': ['sprites/oryx/floor3.png'], 'b': ['sprites/oryx/floor3.png', 'sprites/oryx/door2.png'],
                'c': ['sprites/oryx/floor3.png', 'sprites/oryx/swordman1_0.png'],
                'd': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png'],
                'e': ['sprites/oryx/floor3.png', 'sprites/oryx/key2.png'],
                'f': ['sprites/oryx/floor3.png', 'sprites/oryx/swordman1_0.png', 'sprites/oryx/slash1.png'],
                'g': ['sprites/oryx/floor3.png', 'sprites/oryx/swordmankey1_0.png'],
                'h': ['sprites/oryx/floor3.png', 'sprites/oryx/swordman1_0.png', 'sprites/oryx/spider2.png'],
                'i': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png', 'sprites/oryx/slash1.png'],
                'j': ['sprites/oryx/floor3.png', 'sprites/oryx/spider2.png', 'sprites/oryx/door2.png'],
                'k': ['sprites/oryx/floor3.png', 'sprites/oryx/spider2.png', 'sprites/oryx/gold2.png'],
                'l': ['sprites/oryx/floor3.png', 'sprites/oryx/gold2.png'],
                'm': ['sprites/oryx/floor3.png', 'sprites/oryx/slash1.png'],
                'n': ['sprites/oryx/floor3.png', 'sprites/oryx/spider2.png', 'sprites/oryx/spider2.png'],
                'o': ['sprites/oryx/floor3.png', 'sprites/oryx/spider2.png'],
                'p': ['sprites/oryx/floor3.png', 'sprites/oryx/doorclosed1.png']}

    if game == 'defem':
        return {'a': ['sprites/oryx/backLBrown.png'],
                'b': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png', 'sprites/newset/hole1.png'],
                'c': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axeman1.png', 'sprites/oryx/axe1.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak2.png', 'sprites/newset/hole5.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak1.png', 'sprites/oryx/axeman1.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axe1.png', 'sprites/newset/hole1.png'],
                'h': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axeman1.png', 'sprites/oryx/axe1.png',
                      'sprites/oryx/axe1.png', 'sprites/oryx/axe1.png'],
                'i': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png', 'sprites/oryx/freak2.png'],
                'j': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png'],
                'k': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak2.png'],
                'l': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axe1.png'],
                'm': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axe1.png', 'sprites/oryx/axe1.png'],
                'n': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png', 'sprites/oryx/freak1.png',
                      'sprites/oryx/freak1.png'],
                'o': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak2.png', 'sprites/oryx/axeman1.png'],
                'p': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak1.png', 'sprites/newset/hole1.png'],
                'q': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png'],
                'r': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak1.png', 'sprites/oryx/freak1.png',
                      'sprites/newset/hole1.png'], 's': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak1.png'],
                't': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axeman1.png'],
                'u': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axe1.png', 'sprites/newset/hole5.png'],
                'v': ['sprites/oryx/backLBrown.png', 'sprites/oryx/axeman1.png', 'sprites/oryx/axe1.png',
                      'sprites/oryx/axe1.png'],
                'w': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak2.png', 'sprites/oryx/freak1.png'],
                'x': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak2.png', 'sprites/newset/hole1.png'],
                'y': ['sprites/oryx/backLBrown.png', 'sprites/oryx/freak3.png'],
                'z': ['sprites/oryx/backLBrown.png', 'sprites/newset/hole1.png']}

    if game == 'doorkoban':
        return {'a': ['sprites/newset/floor2.png'], 'b': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png'],
                'c': ['sprites/newset/floor2.png'], 'd': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png'],
                'e': ['sprites/newset/floor2.png'], 'f': ['sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png'], 'h': ['sprites/newset/floor2.png', 'sprites/newset/block2.png'],
                'i': ['sprites/newset/floor2.png'], 'j': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png'],
                'k': ['sprites/newset/floor2.png', 'sprites/oryx/dooropen1.png'],
                'l': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png'], 'm': ['sprites/newset/floor2.png'],
                'n': ['sprites/newset/floor2.png'], 'o': ['sprites/newset/floor2.png', 'sprites/newset/block2.png'],
                'p': ['sprites/newset/floor2.png'], 'q': ['sprites/newset/floor2.png', 'sprites/newset/block2.png'],
                'r': ['sprites/newset/floor2.png', 'sprites/newset/block2.png']}

    if game == 'escape':
        return {'a': ['sprites/oryx/backLBrown.png'],
                'b': ['sprites/oryx/backLBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'c': ['sprites/oryx/backLBrown.png', 'sprites/oryx/rat1.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/oryx/rat1.png', 'sprites/newset/hole1.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/newset/block3.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/newset/hole1.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/newset/cheese.png']}

    if game == 'fireman':
        return {'a': ['sprites/newset/street3.png'], 'b': ['sprites/newset/street3.png', 'sprites/oryx/wall1.png'],
                'c': ['sprites/newset/street3.png', 'sprites/newset/fireman.png'],
                'd': ['sprites/newset/street3.png', 'sprites/newset/hydrant.png', 'sprites/newset/fireman.png'],
                'e': ['sprites/newset/street3.png', 'sprites/oryx/slime1.png', 'sprites/newset/hydrant.png'],
                'f': ['sprites/newset/street3.png', 'sprites/newset/city1.png'],
                'g': ['sprites/newset/street3.png', 'sprites/newset/city1_fire.png'],
                'h': ['sprites/newset/street3.png', 'sprites/newset/hydrant.png'],
                'i': ['sprites/newset/street3.png', 'sprites/newset/city1_fire.png'],
                'j': ['sprites/newset/street3.png', 'sprites/oryx/slime1.png'],
                'k': ['sprites/newset/street3.png', 'sprites/newset/city1_fire.png'],
                'l': ['sprites/newset/street3.png', 'sprites/newset/fireman.png', 'sprites/newset/city1_fire.png']}

    if game == 'flower':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/mushroom2.png', 'sprites/oryx/dirtWall_12.png',
                      'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/dirtWall_12.png', 'sprites/newset/man1.png',
                      'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/mushroom2.png', 'sprites/oryx/dirtWall_12.png',
                      'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/newset/man1.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/mushroom2.png', 'sprites/oryx/dirtWall_12.png',
                      'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/oryx/mushroom2.png', 'sprites/oryx/mushroom2.png',
                      'sprites/oryx/dirtWall_12.png', 'sprites/newset/floor2.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/oryx/mushroom2.png', 'sprites/oryx/dirtWall_12.png',
                      'sprites/newset/floor2.png'], 'i': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'j': ['sprites/newset/floor2.png', 'sprites/oryx/dirtWall_12.png', 'sprites/newset/floor2.png']}

    if game == 'garbagecollector':
        return {'a': ['sprites/oryx/backGrey.png'],
                'b': ['sprites/oryx/backGrey.png', 'sprites/oryx/dirtWall_15.png', 'sprites/oryx/butcher1.png'],
                'c': ['sprites/oryx/backGrey.png', 'sprites/oryx/wall6.png'],
                'd': ['sprites/oryx/backGrey.png', 'sprites/oryx/dirtWall_15.png'],
                'e': ['sprites/oryx/backGrey.png', 'sprites/oryx/slime5.png'],
                'f': ['sprites/oryx/backGrey.png', 'sprites/oryx/butcher1.png'],
                'g': ['sprites/oryx/backGrey.png', 'sprites/oryx/wall6.png', 'sprites/oryx/butcher1.png']}

    if game == 'hungrybirds':
        return {'a': ['sprites/oryx/grass_15.png'], 'b': ['sprites/oryx/grass_15.png', 'sprites/newset/exit2.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/worm1.png', 'sprites/oryx/worm1.png',
                      'sprites/oryx/worm1.png'], 'd': ['sprites/oryx/grass_15.png', 'sprites/oryx/tree2.png'],
                'e': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png']}

    if game == 'iceandfire':
        return {'a': ['sprites/oryx/grass_15.png'], 'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/tree1.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/backGrey.png'],
                'd': ['sprites/oryx/grass_15.png', 'sprites/oryx/dwarf1.png'],
                'e': ['sprites/oryx/grass_15.png', 'sprites/oryx/gold1.png'],
                'f': ['sprites/oryx/grass_15.png', 'sprites/oryx/fire1.png'],
                'g': ['sprites/oryx/grass_15.png', 'sprites/oryx/boots2.png'],
                'h': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png'],
                'i': ['sprites/oryx/grass_15.png', 'sprites/oryx/dwarf1.png', 'sprites/oryx/backGrey.png'],
                'j': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png'],
                'k': ['sprites/oryx/grass_15.png', 'sprites/oryx/fire1.png', 'sprites/oryx/dwarf1.png'],
                'l': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png', 'sprites/oryx/dwarf1.png'],
                'm': ['sprites/oryx/grass_15.png', 'sprites/oryx/boots3.png']}

    if game == 'invest':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/queen1.png', 'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/newset/man3.png', 'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/oryx/rogue.png', 'sprites/newset/floor2.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/newset/man3.png', 'sprites/newset/floor2.png',
                      'sprites/newset/floor2.png']}

    if game == 'investdie':
        return {'a': ['sprites/newset/floor2.png', 'sprites/newset/man3.png', 'sprites/newset/floor2.png',
                      'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/queen1.png', 'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/newset/man3.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/oryx/rogue.png', 'sprites/newset/floor2.png']}

    if game == 'islands':
        return {'a': ['sprites/newset/water2_1.png', 'sprites/oryx/backLBrown.png', 'sprites/newset/man3.png'],
                'b': ['sprites/newset/water2_1.png', 'sprites/oryx/pickaxe.png'],
                'c': ['sprites/newset/water2_1.png', 'sprites/oryx/wall4.png', 'sprites/oryx/pickaxe.png',
                      'sprites/oryx/backLBrown.png'],
                'd': ['sprites/newset/water2_1.png', 'sprites/oryx/wall4.png', 'sprites/oryx/backLBrown.png'],
                'e': ['sprites/newset/water2_1.png', 'sprites/oryx/backBiege.png', 'sprites/newset/man3.png'],
                'f': ['sprites/newset/water2_1.png', 'sprites/oryx/treasure2.png', 'sprites/oryx/backBiege.png'],
                'g': ['sprites/newset/water2_1.png', 'sprites/newset/bomb.png'],
                'h': ['sprites/newset/water2_1.png', 'sprites/oryx/backBiege.png'],
                'i': ['sprites/newset/water2_1.png'],
                'j': ['sprites/newset/water2_1.png', 'sprites/newset/whirlpool2.png'],
                'k': ['sprites/newset/water2_1.png', 'sprites/oryx/pickaxe.png', 'sprites/oryx/backLBrown.png',
                      'sprites/newset/man3.png'],
                'l': ['sprites/newset/water2_1.png', 'sprites/oryx/backLBrown.png'],
                'm': ['sprites/newset/water2_1.png', 'sprites/oryx/backBiege.png', 'sprites/newset/hole1.png'],
                'n': ['sprites/newset/water2_1.png', 'sprites/oryx/pickaxe.png', 'sprites/oryx/pickaxe.png']}

    if game == 'killBillVol1':
        return {'a': ['sprites/oryx/floor3.png'], 'b': ['sprites/oryx/floor3.png', 'sprites/oryx/doorclosed1.png'],
                'c': ['sprites/oryx/floor3.png', 'sprites/oryx/guard1.png'],
                'd': ['sprites/oryx/floor3.png', 'sprites/oryx/guard1.png', 'sprites/oryx/guard1.png'],
                'e': ['sprites/oryx/floor3.png', 'sprites/oryx/bookDown.png'], 'f': ['sprites/oryx/floor3.png'],
                'g': ['sprites/oryx/floor3.png', 'sprites/oryx/bookUp.png'],
                'h': ['sprites/oryx/floor3.png', 'sprites/oryx/bookUp.png'],
                'i': ['sprites/oryx/floor3.png', 'sprites/oryx/slash1.png', 'sprites/oryx/bookDown.png'],
                'j': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png', 'sprites/oryx/slash1.png'],
                'k': ['sprites/oryx/floor3.png', 'sprites/oryx/slash1.png', 'sprites/oryx/bookUp.png'],
                'l': ['sprites/oryx/floor3.png', 'sprites/oryx/guard1.png'],
                'm': ['sprites/oryx/floor3.png', 'sprites/oryx/swordman1_0.png'],
                'n': ['sprites/oryx/floor3.png', 'sprites/oryx/swordman1_0.png'],
                'o': ['sprites/oryx/floor3.png', 'sprites/oryx/slash1.png'], 'p': ['sprites/oryx/floor3.png'],
                'q': ['sprites/oryx/floor3.png'], 'r': ['sprites/oryx/floor3.png', 'sprites/oryx/slash1.png'],
                's': ['sprites/oryx/floor3.png'], 't': ['sprites/oryx/floor3.png', 'sprites/oryx/guard1.png'],
                'u': ['sprites/oryx/floor3.png', 'sprites/oryx/bookUp.png'],
                'v': ['sprites/oryx/floor3.png', 'sprites/oryx/guard1.png', 'sprites/oryx/guard1.png'],
                'w': ['sprites/oryx/floor3.png', 'sprites/oryx/wall3_15.png'],
                'x': ['sprites/oryx/floor3.png', 'sprites/oryx/bookDown.png'], 'y': ['sprites/oryx/floor3.png'],
                'z': ['sprites/oryx/floor3.png', 'sprites/oryx/swordman1_0.png', 'sprites/oryx/guard1.png']}

    if game == 'labyrinth':
        return {'a': ['sprites/oryx/grass_15.png'], 'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/wall1.png'],
                'd': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png', 'sprites/newset/girl1.png'],
                'e': ['sprites/oryx/grass_15.png', 'sprites/newset/girl1.png'],
                'f': ['sprites/oryx/grass_15.png', 'sprites/newset/exit2.png']}

    if game == 'labyrinthdual':
        return {'a': ['sprites/oryx/grass_15.png'],
                'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/dirtWall_15.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png', 'sprites/newset/girl1.png'],
                'd': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png', 'sprites/oryx/princess1.png'],
                'e': ['sprites/oryx/grass_15.png', 'sprites/newset/exit2.png'],
                'f': ['sprites/oryx/grass_15.png', 'sprites/oryx/wall1.png'],
                'g': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png'],
                'h': ['sprites/oryx/grass_15.png', 'sprites/newset/girl1.png'],
                'i': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png', 'sprites/oryx/dirtWall_15.png'],
                'j': ['sprites/oryx/grass_15.png', 'sprites/oryx/cloak2.png'],
                'k': ['sprites/oryx/grass_15.png', 'sprites/oryx/cloak3.png'],
                'l': ['sprites/oryx/grass_15.png', 'sprites/oryx/wall3_15.png'],
                'm': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png']}

    if game == 'lemmings':
        return {'a': ['sprites/oryx/backOBrown.png', 'sprites/oryx/dirtWall_15.png', 'sprites/oryx/backOBrown.png'],
                'b': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/backOBrown.png'],
                'c': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/backOBrown.png'],
                'd': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png',
                      'sprites/newset/hole5.png'],
                'e': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png'],
                'f': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png',
                      'sprites/oryx/axeman1.png'],
                'g': ['sprites/oryx/backOBrown.png', 'sprites/oryx/pickaxe.png', 'sprites/oryx/backOBrown.png',
                      'sprites/newset/hole5.png'],
                'h': ['sprites/oryx/backOBrown.png', 'sprites/oryx/door2.png', 'sprites/oryx/backOBrown.png'],
                'i': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axeman1.png',
                      'sprites/newset/hole1.png'],
                'j': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/pickaxe.png', 'sprites/oryx/backOBrown.png'],
                'k': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png'],
                'l': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/backOBrown.png', 'sprites/oryx/axeman1.png'],
                'm': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axeman1.png',
                      'sprites/newset/hole5.png'],
                'n': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png'],
                'o': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png'],
                'p': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/pickaxe.png', 'sprites/oryx/backOBrown.png'],
                'q': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/pickaxe.png',
                      'sprites/oryx/backOBrown.png'],
                'r': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png'],
                's': ['sprites/oryx/backOBrown.png', 'sprites/oryx/pickaxe.png', 'sprites/oryx/backOBrown.png'],
                't': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axeman1.png'],
                'u': ['sprites/oryx/backOBrown.png', 'sprites/oryx/pickaxe.png', 'sprites/oryx/backOBrown.png',
                      'sprites/oryx/axeman1.png'],
                'v': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/spelunky_0.png', 'sprites/oryx/backOBrown.png'],
                'w': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/backOBrown.png', 'sprites/oryx/axeman1.png'],
                'x': ['sprites/oryx/backOBrown.png', 'sprites/oryx/spelunky_0.png', 'sprites/oryx/spelunky_0.png',
                      'sprites/oryx/backOBrown.png'],
                'y': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                'z': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/newset/hole5.png']}

    if game == 'realsokoban':
        return {'a': ['sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/oryx/cspell4.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/cspell4.png', 'sprites/newset/block1.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/cspell4.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/newset/block2.png']}

    if game == 'rivers':
        return {'a': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png'],
                'b': ['sprites/oryx/backOBrown.png', 'sprites/oryx/dirtWall_15.png', 'sprites/oryx/axe2.png'],
                'c': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png',
                      'sprites/newset/man1.png'],
                'd': ['sprites/oryx/backOBrown.png', 'sprites/oryx/dirtWall_15.png', 'sprites/oryx/axe2.png',
                      'sprites/oryx/axe2.png'],
                'e': ['sprites/oryx/backOBrown.png', 'sprites/oryx/tree2.png', 'sprites/oryx/backOBrown.png',
                      'sprites/newset/man1.png'],
                'f': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png',
                      'sprites/newset/man1.png'],
                'g': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cloak1.png', 'sprites/oryx/backOBrown.png',
                      'sprites/oryx/axe2.png'],
                'h': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png'],
                'i': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/newset/man1.png'],
                'j': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                'k': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png',
                      'sprites/oryx/axe2.png'],
                'l': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cloak1.png', 'sprites/oryx/backOBrown.png',
                      'sprites/oryx/axe2.png', 'sprites/oryx/axe2.png'],
                'm': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                'n': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/newset/man1.png'],
                'o': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png'],
                'p': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png',
                      'sprites/oryx/axe2.png'], 'q': ['sprites/oryx/backOBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'r': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png'],
                's': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                't': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/newset/man1.png'],
                'u': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png'],
                'v': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                'w': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                'x': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png'],
                'y': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png'],
                'z': ['sprites/oryx/backOBrown.png', 'sprites/oryx/backOBrown.png', 'sprites/oryx/axe2.png']}

    if game == 'run':
        return {'a': ['sprites/oryx/backLBrown.png', 'sprites/newset/water2.png', 'sprites/newset/girl2.png'],
                'b': ['sprites/oryx/backLBrown.png', 'sprites/newset/water2.png'],
                'c': ['sprites/oryx/backLBrown.png', 'sprites/oryx/door2.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/newset/water2.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/newset/water5.png', 'sprites/newset/water2.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/newset/water5.png', 'sprites/newset/water2.png',
                      'sprites/newset/girl2.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/newset/water2.png', 'sprites/newset/lock1.png'],
                'h': ['sprites/oryx/backLBrown.png', 'sprites/newset/water2.png', 'sprites/newset/girl2.png'],
                'i': ['sprites/oryx/backLBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'j': ['sprites/oryx/backLBrown.png', 'sprites/oryx/key2.png', 'sprites/newset/water2.png']}

    if game == 'shipwreck':
        return {'a': ['sprites/newset/water3.png', 'sprites/newset/dock2.png'],
                'b': ['sprites/newset/water3.png', 'sprites/newset/whirlpool2.png', 'sprites/newset/ship.png'],
                'c': ['sprites/newset/water3.png', 'sprites/oryx/goldsack.png', 'sprites/oryx/diamond2.png',
                      'sprites/newset/shipwreck.png'], 'd': ['sprites/newset/water3.png', 'sprites/oryx/grass_15.png'],
                'e': ['sprites/newset/water3.png', 'sprites/newset/ship.png'],
                'f': ['sprites/newset/water3.png', 'sprites/oryx/goldsack.png', 'sprites/oryx/gold2.png',
                      'sprites/oryx/diamond2.png', 'sprites/newset/shipwreck.png'],
                'g': ['sprites/newset/water3.png', 'sprites/newset/whirlpool2.png'],
                'h': ['sprites/newset/water3.png', 'sprites/newset/shipwreck.png'],
                'i': ['sprites/newset/water3.png', 'sprites/oryx/diamond2.png', 'sprites/newset/shipwreck.png'],
                'j': ['sprites/newset/water3.png', 'sprites/newset/dock3.png'],
                'k': ['sprites/newset/water3.png', 'sprites/oryx/gold2.png', 'sprites/newset/shipwreck.png'],
                'l': ['sprites/newset/water3.png', 'sprites/newset/dock1.png'],
                'm': ['sprites/newset/water3.png', 'sprites/newset/ship.png', 'sprites/newset/dock2.png'],
                'n': ['sprites/newset/water3.png', 'sprites/oryx/goldsack.png', 'sprites/oryx/gold2.png',
                      'sprites/newset/shipwreck.png'], 'o': ['sprites/newset/water3.png'],
                'p': ['sprites/newset/water3.png', 'sprites/oryx/gold2.png', 'sprites/oryx/diamond2.png',
                      'sprites/newset/shipwreck.png']}

    if game == 'sistersavior':
        return {'a': ['sprites/newset/floor5.png', 'sprites/oryx/cspell3.png', 'sprites/newset/floor5.png'],
                'b': ['sprites/newset/floor5.png', 'sprites/oryx/wall3_15.png', 'sprites/oryx/cspell3.png'],
                'c': ['sprites/newset/floor5.png', 'sprites/newset/floor5.png'],
                'd': ['sprites/newset/floor5.png', 'sprites/oryx/scorpion1.png', 'sprites/newset/man1.png',
                      'sprites/newset/floor5.png'],
                'e': ['sprites/newset/floor5.png', 'sprites/oryx/scorpion1.png', 'sprites/oryx/cspell3.png',
                      'sprites/newset/floor5.png'],
                'f': ['sprites/newset/floor5.png', 'sprites/oryx/scorpion1.png', 'sprites/newset/floor5.png'],
                'g': ['sprites/newset/floor5.png', 'sprites/oryx/wall3_15.png'],
                'h': ['sprites/newset/floor5.png', 'sprites/newset/girl3.png', 'sprites/newset/floor5.png'],
                'i': ['sprites/newset/floor5.png', 'sprites/newset/man1.png', 'sprites/newset/floor5.png']}

    if game == 'sokoban':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png', 'sprites/newset/block1.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/oryx/cspell4.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/oryx/cspell4.png',
                      'sprites/newset/floor2.png']}

    if game == 'surround':
        return {'a': ['sprites/oryx/backGrey.png', 'sprites/oryx/floorTileGreen.png'],
                'b': ['sprites/oryx/backGrey.png', 'sprites/oryx/yeti1.png', 'sprites/oryx/floorTileGreen.png'],
                'c': ['sprites/oryx/backGrey.png'], 'd': ['sprites/oryx/backGrey.png', 'sprites/oryx/dirtWall_15.png'],
                'e': ['sprites/oryx/backGrey.png', 'sprites/oryx/wolf1.png', 'sprites/oryx/floorTileOrange.png'],
                'f': ['sprites/oryx/backGrey.png']}

    if game == 'tercio':
        return {'a': ['sprites/oryx/backBlack.png', 'sprites/oryx/backBlue.png', 'sprites/newset/hole1.png'],
                'b': ['sprites/oryx/backBlack.png', 'sprites/oryx/backGrey.png'],
                'c': ['sprites/oryx/backBlack.png', 'sprites/oryx/backGrey.png', 'sprites/newset/hole1.png'],
                'd': ['sprites/oryx/backBlack.png', 'sprites/oryx/backBlue.png', 'sprites/newset/girl3.png'],
                'e': ['sprites/oryx/backBlack.png', 'sprites/oryx/backGrey.png', 'sprites/newset/hole1.png',
                      'sprites/newset/girl1.png'], 'f': ['sprites/oryx/backBlack.png', 'sprites/oryx/dirtWall_15.png'],
                'g': ['sprites/oryx/backBlack.png', 'sprites/oryx/bush5.png', 'sprites/oryx/backBlue.png'],
                'h': ['sprites/oryx/backBlack.png'],
                'i': ['sprites/oryx/backBlack.png', 'sprites/oryx/backOBrown.png', 'sprites/newset/girl4.png'],
                'j': ['sprites/oryx/backBlack.png', 'sprites/oryx/backBlue.png', 'sprites/newset/hole1.png',
                      'sprites/newset/girl3.png'], 'k': ['sprites/oryx/backBlack.png', 'sprites/oryx/backBlue.png'],
                'l': ['sprites/oryx/backBlack.png', 'sprites/oryx/backGrey.png', 'sprites/newset/girl1.png'],
                'm': ['sprites/oryx/backBlack.png', 'sprites/oryx/bush5.png', 'sprites/oryx/backGrey.png'],
                'n': ['sprites/oryx/backBlack.png', 'sprites/newset/girl2.png'],
                'o': ['sprites/oryx/backBlack.png', 'sprites/oryx/bush5.png'],
                'p': ['sprites/oryx/backBlack.png', 'sprites/oryx/backOBrown.png'],
                'q': ['sprites/oryx/backBlack.png', 'sprites/oryx/bush5.png', 'sprites/oryx/backOBrown.png']}

    if game == 'testgame2':
        return {'a': ['sprites/newset/floor2.png', 'sprites/oryx/staff2.png', 'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/necromancer1.png', 'sprites/oryx/cspell1.png',
                      'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/necromancer1.png', 'sprites/oryx/cspell2.png',
                      'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/oryx/cspell2.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/cspell1.png', 'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/oryx/staff2.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/oryx/staff2.png', 'sprites/oryx/necromancer1.png',
                      'sprites/newset/floor2.png'], 'i': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png'],
                'j': ['sprites/newset/floor2.png', 'sprites/oryx/necromancer1.png', 'sprites/newset/floor2.png']}

    if game == 'testgame3':
        return {'a': ['sprites/newset/floor2.png', 'sprites/newset/floor3.png', 'sprites/newset/floor2.png'],
                'b': ['sprites/newset/floor2.png', 'sprites/oryx/wall3_15.png', 'sprites/newset/floor2.png'],
                'c': ['sprites/newset/floor2.png', 'sprites/oryx/gold1.png', 'sprites/newset/floor2.png'],
                'd': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png'],
                'e': ['sprites/newset/floor2.png', 'sprites/newset/floor2.png', 'sprites/newset/block1.png'],
                'f': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/newset/floor2.png'],
                'g': ['sprites/newset/floor2.png', 'sprites/oryx/cspell4.png', 'sprites/newset/floor2.png'],
                'h': ['sprites/newset/floor2.png', 'sprites/oryx/knight1.png', 'sprites/oryx/cspell4.png',
                      'sprites/newset/floor2.png']}

    if game == 'thecitadel':
        return {'a': ['sprites/oryx/backLBrown.png'], 'b': ['sprites/oryx/backLBrown.png', 'sprites/oryx/barrel1.png'],
                'c': ['sprites/oryx/backLBrown.png', 'sprites/newset/hole4.png'],
                'd': ['sprites/oryx/backLBrown.png', 'sprites/newset/hole5.png'],
                'e': ['sprites/oryx/backLBrown.png', 'sprites/oryx/wall2.png'],
                'f': ['sprites/oryx/backLBrown.png', 'sprites/oryx/spelunky_0.png'],
                'g': ['sprites/oryx/backLBrown.png', 'sprites/oryx/dirtWall_15.png'],
                'h': ['sprites/oryx/backLBrown.png', 'sprites/oryx/door2.png']}

    if game == 'theshepherd':
        return {'a': ['sprites/oryx/grass_15.png'], 'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png'],
                'c': ['sprites/oryx/grass_15.png', 'sprites/oryx/belt2.png'],
                'd': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png', 'sprites/oryx/bird1.png'],
                'e': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird2.png', 'sprites/oryx/bird2.png',
                      'sprites/oryx/bird2.png'], 'f': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png'],
                'g': ['sprites/oryx/grass_15.png', 'sprites/oryx/spike2.png'],
                'h': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png', 'sprites/oryx/belt2.png'],
                'i': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird2.png'],
                'j': ['sprites/oryx/grass_15.png', 'sprites/oryx/belt2.png'],
                'k': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png', 'sprites/oryx/bird1.png'],
                'l': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png'],
                'm': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird2.png'], 'n': ['sprites/oryx/grass_15.png'],
                'o': ['sprites/oryx/grass_15.png', 'sprites/oryx/tree2.png'],
                'p': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png'],
                'q': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png'],
                'r': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png', 'sprites/oryx/belt2.png'],
                's': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png'],
                't': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png'],
                'u': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png', 'sprites/oryx/belt2.png'],
                'v': ['sprites/oryx/grass_15.png', 'sprites/oryx/princess1.png'],
                'w': ['sprites/oryx/grass_15.png', 'sprites/oryx/belt2.png'],
                'x': ['sprites/oryx/grass_15.png', 'sprites/oryx/belt2.png'],
                'y': ['sprites/oryx/grass_15.png', 'sprites/oryx/bird1.png', 'sprites/oryx/bird1.png'],
                'z': ['sprites/oryx/grass_15.png']}

    if game == 'thesnowman':
        return {'a': ['sprites/oryx/backGrey.png'],
                'b': ['sprites/oryx/backGrey.png', 'sprites/newset/winterelf1.png', 'sprites/newset/snowmanbase.png'],
                'c': ['sprites/oryx/backGrey.png', 'sprites/newset/snowmanbody.png'],
                'd': ['sprites/oryx/backGrey.png', 'sprites/newset/snowmanbase.png'],
                'e': ['sprites/oryx/backGrey.png', 'sprites/oryx/key2.png'],
                'f': ['sprites/oryx/backGrey.png', 'sprites/oryx/wall3_15.png'],
                'g': ['sprites/oryx/backGrey.png', 'sprites/newset/lock1.png'],
                'h': ['sprites/oryx/backGrey.png', 'sprites/newset/snowmanchest.png'],
                'i': ['sprites/oryx/backGrey.png', 'sprites/newset/winterelf1.png'],
                'j': ['sprites/oryx/backGrey.png', 'sprites/newset/snowmanhead.png']}

    if game == 'vortex':
        return {'a': ['sprites/oryx/grass_15.png'], 'b': ['sprites/oryx/grass_15.png', 'sprites/oryx/treasure2.png'],
                'c': ['sprites/oryx/grass_15.png'], 'd': ['sprites/oryx/grass_15.png'],
                'e': ['sprites/oryx/grass_15.png'], 'f': ['sprites/oryx/grass_15.png', 'sprites/oryx/tree1.png'],
                'g': ['sprites/oryx/grass_15.png', 'sprites/newset/whirlpool2.png'],
                'h': ['sprites/oryx/grass_15.png', 'sprites/newset/man3.png'],
                'i': ['sprites/oryx/grass_15.png', 'sprites/oryx/dooropen1.png'],
                'j': ['sprites/oryx/grass_15.png', 'sprites/newset/whirlpool2.png', 'sprites/newset/man4.png'],
                'k': ['sprites/oryx/grass_15.png', 'sprites/newset/man4.png'],
                'l': ['sprites/oryx/grass_15.png', 'sprites/newset/man3.png'],
                'm': ['sprites/oryx/grass_15.png', 'sprites/newset/man3.png'],
                'n': ['sprites/oryx/grass_15.png', 'sprites/newset/man3.png'],
                'o': ['sprites/oryx/grass_15.png', 'sprites/newset/block3.png'], 'p': ['sprites/oryx/grass_15.png']}

    if game == 'waferthinmints':
        return {'a': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/niceGuy.png',
                      'sprites/newset/chef.png'],
                'b': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/butter.png'],
                'c': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/chef.png',
                      'sprites/newset/butter.png'], 'd': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png'],
                'e': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/chef.png'],
                'f': ['sprites/newset/tile3.png', 'sprites/newset/wallRed.png'],
                'g': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/niceGuy.png']}

    if game == 'waferthinmintsexit':
        return {'a': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/butter.png'],
                'b': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png'],
                'c': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/exit.png'],
                'd': ['sprites/newset/tile3.png', 'sprites/newset/wallRed.png'],
                'e': ['sprites/newset/tile3.png', 'sprites/newset/tile3.png', 'sprites/newset/niceGuy.png']}

    if game == 'watergame':
        return {'a': ['sprites/oryx/floor4.png'], 'b': ['sprites/oryx/floor4.png', 'sprites/oryx/mage1.png'],
                'c': ['sprites/oryx/floor4.png', 'sprites/newset/water.png'],
                'd': ['sprites/oryx/floor4.png', 'sprites/oryx/door2.png'],
                'e': ['sprites/oryx/floor4.png', 'sprites/oryx/potion1.png'],
                'f': ['sprites/oryx/floor4.png', 'sprites/oryx/wall6.png'],
                'g': ['sprites/oryx/floor4.png', 'sprites/oryx/mage1.png', 'sprites/newset/water.png']}

    if game == 'painter':
        return {'a': ['sprites/oryx/backGrey.png', 'sprites/newset/floor5.png'],
                'b': ['sprites/oryx/backGrey.png', 'sprites/newset/paint2.png'],
                'c': ['sprites/oryx/backGrey.png', 'sprites/newset/painter21.png', 'sprites/newset/paint2.png'],
                'd': ['sprites/oryx/backGrey.png', 'sprites/oryx/backGrey.png'],
                'e': ['sprites/oryx/backGrey.png', 'sprites/newset/paint2.png'],
                'f': ['sprites/oryx/backGrey.png', 'sprites/oryx/backGrey.png'],
                'g': ['sprites/oryx/backGrey.png', 'sprites/newset/painter21.png', 'sprites/newset/floor5.png'],
                'h': ['sprites/oryx/backGrey.png', 'sprites/oryx/backGrey.png', 'sprites/newset/painter21.png']}

    if game == 'whackamole':
        return {'a': ['sprites/oryx/backOBrown.png', 'sprites/newset/mole_slow.png', 'sprites/newset/hole1.png'],
                'b': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cyclop1.png', 'sprites/newset/hole4.png',
                      'sprites/newset/cat.png'], 'c': ['sprites/oryx/backOBrown.png', 'sprites/newset/hole4.png'],
                'd': ['sprites/oryx/backOBrown.png', 'sprites/newset/hole1.png', 'sprites/newset/cat.png'],
                'e': ['sprites/oryx/backOBrown.png', 'sprites/newset/mole_fast.png', 'sprites/newset/mole_fast.png',
                      'sprites/newset/hole4.png'],
                'f': ['sprites/oryx/backOBrown.png', 'sprites/newset/mole_fast.png', 'sprites/newset/hole4.png'],
                'g': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cyclop1.png', 'sprites/newset/cat.png'],
                'h': ['sprites/oryx/backOBrown.png'], 'i': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cyclop1.png'],
                'j': ['sprites/oryx/backOBrown.png', 'sprites/newset/hole4.png', 'sprites/newset/cat.png'],
                'k': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cyclop1.png', 'sprites/newset/hole4.png'],
                'l': ['sprites/oryx/backOBrown.png', 'sprites/oryx/cyclop1.png', 'sprites/newset/hole1.png'],
                'm': ['sprites/oryx/backOBrown.png', 'sprites/newset/cat.png'],
                'n': ['sprites/oryx/backOBrown.png', 'sprites/newset/hole1.png']}
    return {x: y for x,y in zip(range(30), range(30))}


def get_object_dict(game):
    if game == "sokoban":
        return {"floor box": "b",
                "wall floor": "w",
                "floor hole": "h",
                "avatar floor": "a",
                "avatar floor hole": "A",
                "floor": " "}
    if game == "butterflies":
        return {"butterfly": "b",
                "wall": "w",
                "cocoon": "c",
                "avatar": "a",
                "": " "}
    if game == "aliens":
        return {'': " ",
                'avatar': "a",
                'base': "b",
                'bomb alienGreen portalFast': "c",
                'sam': "s",
                'bomb alienGreen': "e",
                'alienGreen portalFast': "f",
                'portalFast': "g",
                'bomb alienBlue portalSlow': "h",
                'avatar sam': "i",
                'bomb alienBlue': "j",
                'alienBlue portalSlow': "k",
                'portalSlow': "l",
                'alienGreen': "m",
                'alienBlue': "n"}

    if game == 'painter':
        return {'wall': 'a', 'paint prepaint': 'b', 'avatar paint preground': 'c', 'ground': 'd', 'paint': 'e',
                'ground preground': 'f', 'wall avatar': 'g', 'avatar ground prepaint': 'h'}

    if game == 'bait':
        return {'': 'a', 'nokey': 'b', 'goal': 'c', 'hole nokey': 'd', 'wall': 'e', 'box': 'f', 'hole': 'g',
                'mushroom': 'h', 'key box': 'i', 'key': 'j'}

    if game == 'bait':
        return {'nokey': 'a', 'goal': 'b', '': 'c', 'wall': 'd', 'key': 'e', 'hole nokey': 'f', 'withkey': 'g',
                'box': 'h', 'mushroom': 'i', 'hole': 'j'}

    if game == 'brainman':
        return {'': 'a', 'green': 'b', 'wall': 'c', 'key': 'd', 'avatar': 'e', 'blue': 'f', 'boulder': 'g',
                'exit': 'h', 'red': 'i', 'door': 'j', 'keym': 'k'}

    if game == 'catapults':
        return {'': 'a', 'eastfacing': 'b', 'goal': 'c', 'east': 'd', 'wall': 'e', 'northfacing': 'f',
                'southfacing': 'g', 'moving': 'h', 'water': 'i', 'water moving': 'j', 'westfacing': 'k',
                'water east': 'l'}

    if game == 'cec2':
        return {'floor lightoff': 'a', 'wall': 'b', 'avatar floor': 'c', 'avatar floor lighton': 'd',
                'avatar floor staff': 'e', 'avatar floor lightoff': 'f', 'floor staff': 'g', 'floor lighton': 'h',
                'wall staff': 'i', 'floor': 'j'}

    if game == 'cec3':
        return {'wall floor': 'a', 'avatar floor': 'b', 'floor box': 'c', 'floor switch': 'd', 'floor coin': 'e',
                'floor hole': 'f', 'floor': 'g'}

    if game == 'chainreaction':
        return {'wall': 'a', 'floor normalBoulder': 'b', 'avatar floor': 'c', 'floor mboulderm': 'd',
                'floor masterBoulder': 'e', 'floor': 'f', 'avatar floor mboulderm': 'g', 'avatar floor hole': 'h',
                'avatar floor masterBoulder': 'i', 'avatar floor goal': 'j', 'floor box': 'k', 'floor goal': 'l',
                'floor hole': 'm'}

    if game == 'chase':
        return {'': 'a', 'scared scared scared scared': 'b', 'avatar angry': 'c', 'wall': 'd', 'scared': 'e',
                'carcass': 'f', 'avatar': 'g', 'angry': 'h', 'scared scared': 'i', 'scared scared scared': 'j',
                'avatar carcass': 'k'}

    if game == 'chipschallenge':
        return {'': 'a', 'greenkey': 'b', 'reddoor': 'c', 'wall': 'd', 'gate': 'e', 'crate': 'f', 'bluekey': 'g',
                'avatar': 'h', 'flippers': 'i', 'chip': 'j', 'yellowdoor': 'k', 'fire': 'l', 'fireboots': 'm',
                'exit': 'n', 'yellowkey': 'o', 'avatar fire': 'p', 'water': 'q', 'greendoor': 'r', 'bluedoor': 's',
                'avatar water': 't', 'redkey': 'u'}

    if game == 'clusters':
        return {'': 'a', 'wall': 'b', 'greenblock': 'c', 'avatar': 'd', 'redblock': 'e', 'redbox': 'f', 'hole': 'g',
                'avatar hole': 'h', 'greenbox': 'i', 'blueblock': 'j', 'bluebox': 'k'}

    if game == 'colourescape':
        return {'': 'a', 'wall': 'b', 'blueSwitch blueAvatar': 'c', 'box': 'd', 'redbox': 'e', 'blueAvatar': 'f',
                'redAvatar': 'g', 'hole blueAvatar': 'h', 'hole': 'i', 'exit': 'j', 'hole redAvatar': 'k',
                'blueSwitch': 'l', 'normalAvatar': 'm', 'redSwitch': 'n', 'hole greenAvatar': 'o', 'greenbox': 'p',
                'greenSwitch greenAvatar': 'q', 'redSwitch redAvatar': 'r', 'normalSwitch': 's', 'greenSwitch': 't',
                'greenAvatar': 'u', 'bluebox': 'v'}

    if game == 'cookmepasta':
        return {'': 'a', 'wall': 'b', 'key': 'c', 'tuna': 'd', 'avatar': 'e', 'lock': 'f', 'tomato': 'g',
                'boilingwater': 'h', 'rawpasta': 'i'}

    if game == 'decepticoins':
        return {'floor coin piranha': 'a', 'wall floor': 'b', 'avatar floor': 'c',
                'floor piranha piranha piranha': 'd', 'floor switch': 'e', 'floor coin': 'f',
                'floor piranha piranha': 'g', 'floor': 'h', 'avatar floor hole': 'i', 'floor box': 'j',
                'floor piranha': 'k', 'floor hole': 'l', 'avatar floor piranha': 'm',
                'floor coin piranha piranha': 'n'}

    if game == 'deceptizelda':
        return {'': 'a', 'largegoal': 'b', 'nokey': 'c', 'wall': 'd', 'key': 'e', 'sword nokey': 'f',
                'withkey': 'g', 'nokey monsterNormal': 'h', 'wall sword': 'i', 'largegoal monsterNormal': 'j',
                'vase monsterNormal': 'k', 'vase': 'l', 'sword': 'm', 'monsterNormal monsterNormal': 'n',
                'monsterNormal': 'o', 'smallgoal': 'p'}

    if game == 'defem':
        return {'': 'a', 'dirEnemy spawnRandom': 'b', 'avatar bullet': 'c', 'chaseEnemy spawnChase': 'd',
                'dirEnemy spawnHorzD': 'e', 'avatar randomEnemy': 'f', 'bullet spawnRandom': 'g',
                'avatar bullet bullet bullet': 'h', 'chaseEnemy dirEnemy': 'i', 'dirEnemy spawnHorzL': 'j',
                'chaseEnemy spawnHorzD': 'k', 'bullet': 'l', 'bullet bullet': 'm',
                'randomEnemy randomEnemy dirEnemy': 'n', 'avatar chaseEnemy': 'o', 'randomEnemy spawnRandom': 'p',
                'dirEnemy': 'q', 'randomEnemy randomEnemy spawnRandom': 'r', 'randomEnemy': 's', 'avatar': 't',
                'bullet spawnChase': 'u', 'avatar bullet bullet': 'v', 'randomEnemy chaseEnemy': 'w',
                'chaseEnemy spawnRandom': 'x', 'dirEnemy spawnHorzR': 'y', 'spawnRandom': 'z'}

    if game == 'doorkoban':
        return {'': 'a', 'wall': 'b', 'door2': 'c', 'avatar': 'd', 'hole0': 'e', 'door1': 'f', 'hole2': 'g',
                'box3': 'h', 'hole3': 'i', 'avatar hole0': 'j', 'exit': 'k', 'avatar hole1': 'l', 'door0': 'm',
                'door3': 'n', 'box1': 'o', 'hole1': 'p', 'box2': 'q', 'box0': 'r'}

    if game == 'escape':
        return {'': 'a', 'wall': 'b', 'avatar': 'c', 'avatar hole': 'd', 'box': 'e', 'hole': 'f', 'exit': 'g'}

    if game == 'fireman':
        return {'': 'a', 'wall': 'b', 'avatar': 'c', 'avatar extinguisher': 'd', 'water extinguisher': 'e',
                'box': 'f', 'fireOn fireStart fireStart': 'g', 'extinguisher': 'h', 'fireOn fireStart': 'i',
                'water': 'j', 'fireOn': 'k', 'avatar fireOn': 'l'}

    if game == 'flower':
        return {'floor seed flower1': 'a', 'avatar floor seed': 'b', 'wall floor': 'c', 'floor seed flower2': 'd',
                'avatar floor': 'e', 'floor seed flower4': 'f', 'floor seed flower1 flower1': 'g',
                'floor seed flower3': 'h', 'floor': 'i', 'floor seed': 'j'}

    if game == 'garbagecollector':
        return {'': 'a', 'wall avatar': 'b', 'playerWall': 'c', 'wall': 'd', 'garbage': 'e', 'avatar': 'f',
                'avatar playerWall': 'g'}

    if game == 'hungrybirds':
        return {'': 'a', 'goal': 'b', 'foodbank food food food': 'c', 'wall': 'd', 'avatar': 'e'}

    if game == 'iceandfire':
        return {'': 'a', 'wall': 'b', 'ice': 'c', 'avatar': 'd', 'chip': 'e', 'fire': 'f', 'fireboots': 'g',
                'exit': 'h', 'avatar ice': 'i', 'trap': 'j', 'avatar fire': 'k', 'avatar trap': 'l',
                'iceshoes': 'm'}

    if game == 'invest':
        return {'wall floor': 'a', 'floor switch3': 'b', 'avatar floor': 'c', 'floor switch2': 'd',
                'floor coin': 'e', 'floor': 'f', 'floor switch1': 'g', 'avatar floor switch2n': 'h'}

    if game == 'investdie':
        return {'avatar floor switch1n': 'a', 'wall floor': 'b', 'floor switch3': 'c', 'avatar floor': 'd',
                'floor switch2': 'e', 'floor coin': 'f', 'floor': 'g', 'floor switch1': 'h'}

    if game == 'islands':
        return {'avatar landNoSand': 'a', 'water shovel': 'b', 'landNoSand shovel sand': 'c',
                'landNoSand sand': 'd', 'avatar landSand': 'e', 'landSand treasure': 'f', 'water bomb': 'g',
                'landSand': 'h', 'water': 'i', 'water whirlpool': 'j', 'avatar landNoSand shovel': 'k',
                'landNoSand': 'l', 'landSand goal': 'm', 'water shovel shovel': 'n'}

    if game == 'killBillVol1':
        return {'': 'a', 'goal': 'b', 'randomEnemy2 chip2': 'c', 'randomEnemy1 randomEnemy1': 'd', 'liftdown': 'e',
                'chip3': 'f', 'liftup up': 'g', 'liftup down': 'h', 'liftdown sword': 'i', 'wall sword': 'j',
                'liftup sword': 'k', 'randomEnemy3': 'l', 'onground': 'm', 'onground trap1': 'n', 'sword': 'o',
                'trap3': 'p', 'chip2': 'q', 'sword chip1': 'r', 'trap2': 's', 'randomEnemy2': 't', 'liftup': 'u',
                'randomEnemy3 randomEnemy3': 'v', 'wall': 'w', 'liftdown down': 'x', 'chip1': 'y',
                'onground randomEnemy3': 'z'}

    if game == 'labyrinth':
        return {'': 'a', 'trap': 'b', 'wall': 'c', 'avatar trap': 'd', 'avatar': 'e', 'exit': 'f'}

    if game == 'labyrinthdual':
        return {'': 'a', 'redWall': 'b', 'trap avatarNormal': 'c', 'trap avatarRed': 'd', 'exit': 'e',
                'normalWall': 'f', 'trap': 'g', 'avatarNormal': 'h', 'redWall avatarRed': 'i', 'redcoat': 'j',
                'bluecoat': 'k', 'blueWall': 'l', 'avatarRed': 'm'}

    if game == 'lemmings':
        return {'wall floor': 'a',
                'floor lemming lemming lemming lemming lemming lemming lemming lemming lemming lemming lemming': 'b',
                'floor lemming lemming lemming lemming lemming lemming lemming lemming': 'c',
                'floor entrance lemming': 'd',
                'floor lemming lemming lemming lemming lemming lemming lemming lemming lemming lemming': 'e',
                'avatar floor lemming': 'f', 'floor shovel entrance': 'g', 'floor exit': 'h',
                'avatar floor hole': 'i', 'floor shovel lemming lemming': 'j',
                'floor lemming lemming lemming lemming lemming lemming': 'k',
                'avatar floor lemming lemming lemming lemming lemming': 'l', 'avatar floor entrance': 'm',
                'floor lemming': 'n', 'floor lemming lemming lemming lemming lemming lemming lemming': 'o',
                'floor shovel lemming lemming lemming lemming lemming': 'p', 'floor shovel lemming': 'q',
                'floor lemming lemming lemming lemming': 'r', 'floor shovel': 's', 'avatar floor': 't',
                'avatar floor shovel': 'u',
                'floor lemming lemming lemming lemming lemming lemming lemming lemming lemming': 'v',
                'avatar floor lemming lemming': 'w', 'floor lemming lemming': 'x', 'floor': 'y',
                'floor entrance': 'z'}
    if game == 'realsokoban':
        return {'': 'a', 'avatar hole': 'b', 'hole boxin': 'c', 'avatar': 'd', 'hole': 'e', 'wall': 'f', 'box': 'g'}

    if game == 'rivers':
        return {
            'floor shovel waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn waterOn waterOn waterOn': 'a',
            'wall shovel': 'b', 'avatar floor shovel waterOn': 'c', 'wall shovel shovel': 'd',
            'avatar floor ground': 'e', 'avatar floor shovel': 'f', 'floor shovel dryHouse': 'g',
            'floor shovel waterStart waterOn': 'h',
            'avatar floor waterStart waterStart waterStart waterOn waterOn waterOn': 'i',
            'floor waterOn waterOn': 'j',
            'floor shovel shovel waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn': 'k',
            'floor shovel shovel dryHouse': 'l',
            'floor waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn': 'm',
            'avatar floor waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn waterOn waterOn waterOn': 'n',
            'floor shovel waterStart waterStart waterStart waterOn waterOn waterOn': 'o',
            'floor shovel shovel waterOn': 'p', 'wall': 'q',
            'floor shovel waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn waterOn waterOn waterOn': 'r',
            'floor waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn waterOn waterOn waterOn': 's',
            'avatar floor': 't',
            'floor shovel waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn': 'u',
            'floor waterStart waterOn': 'v',
            'floor waterStart waterStart waterStart waterStart waterStart waterStart waterOn waterOn waterOn waterOn waterOn waterOn': 'w',
            'floor shovel': 'x', 'floor waterOn': 'y',
            'floor shovel waterStart waterStart waterStart waterStart waterOn waterOn': 'z'}

    if game == 'run':
        return {'avatar cliff ground': 'a', 'cliff ground': 'b', 'ground exit': 'c', 'cliff': 'd',
                'cliff damaged': 'e', 'avatar cliff damaged': 'f', 'cliff ground lock': 'g', 'avatar cliff': 'h',
                'wall': 'i', 'cliff ground key': 'j'}

    if game == 'shipwreck':
        return {'water portGems': 'a', 'avatar water whirlpool': 'b', 'water shipwreck gems diamonds': 'c',
                'water land': 'd', 'avatar water': 'e', 'water shipwreck gold gems diamonds': 'f',
                'water whirlpool': 'g', 'water shipwreck': 'h', 'water shipwreck gems': 'i',
                'water portDiamonds': 'j', 'water shipwreck gold': 'k', 'water portGold': 'l',
                'avatar water portGems': 'm', 'water shipwreck gold diamonds': 'n', 'water': 'o',
                'water shipwreck gold gems': 'p'}

    if game == 'sistersavior':
        return {'floor plas': 'a', 'wall plas': 'b', 'floor': 'c', 'avatar floor bigPop': 'd',
                'floor plas bigPop': 'e', 'floor bigPop': 'f', 'wall': 'g', 'floor littleSister': 'h',
                'avatar floor': 'i'}

    if game == 'sokoban':
        return {'wall floor': 'a', 'floor': 'b', 'floor box': 'c', 'avatar floor': 'd', 'floor hole': 'e',
                'avatar floor hole': 'f'}

    if game == 'surround':
        return {'grass': 'a', 'avatar grass': 'b', 'snow sword': 'c', 'wall': 'd', 'mud dog': 'e', 'snow': 'f'}

    if game == 'tercio':
        return {'blue target': 'a', 'white': 'b', 'white target': 'c', 'blue inBlue': 'd',
                'white target inWhite': 'e', 'wall': 'f', 'blue crate': 'g', 'black': 'h', 'grey inGrey': 'i',
                'blue target inBlue': 'j', 'blue': 'k', 'white inWhite': 'l', 'white crate': 'm',
                'black inBlack': 'n', 'black crate': 'o', 'grey': 'p', 'grey crate': 'q'}

    if game == 'testgame2':
        return {'floor staff': 'a', 'avatar floor lightoff': 'b', 'avatar floor lighton': 'c', 'floor lighton': 'd',
                'floor': 'e', 'floor lightoff': 'f', 'wall staff': 'g', 'avatar floor staff': 'h', 'wall': 'i',
                'avatar floor': 'j'}

    if game == 'testgame3':
        return {'floor switch': 'a', 'wall floor': 'b', 'floor coin': 'c', 'floor': 'd', 'floor box': 'e',
                'avatar floor': 'f', 'floor hole': 'g', 'avatar floor hole': 'h'}

    if game == 'thecitadel':
        return {'': 'a', 'boulder': 'b', 'roundhole': 'c', 'squarehole': 'd', 'crate': 'e', 'avatar': 'f',
                'wall': 'g', 'goal': 'h'}

    if game == 'theshepherd':
        return {'': 'a', 'hungry door': 'b', 'help treats': 'c', 'scared door': 'd', 'tamed tamed tamed': 'e',
                'scared': 'f', 'fence': 'g', 'avatar treats': 'h', 'tamed hungry': 'i', 'treats': 'j',
                'seeking door': 'k', 'avatar hungry': 'l', 'tamed': 'm', 'help': 'n', 'wall': 'o', 'seeking': 'p',
                'help door': 'q', 'scared hungry treats': 'r', 'door': 's', 'seeking hungry': 't',
                'scared treats': 'u', 'avatar': 'v', 'dogtreat': 'w', 'hungry treats': 'x', 'scared scared': 'y',
                'hungry': 'z'}

    if game == 'thesnowman':
        return {'': 'a', 'avatar base': 'b', 'body': 'c', 'base': 'd', 'key': 'e', 'wall': 'f', 'lock': 'g',
                'chest': 'h', 'avatar': 'i', 'head': 'j'}

    if game == 'vortex':
        return {'': 'a', 'treasure': 'b', 'westfacing': 'c', 'eastfacing': 'd', 'southfacing': 'e', 'wall': 'f',
                'stopvortex': 'g', 'eastfacing falling': 'h', 'exit': 'i', 'stopvortex moving': 'j', 'moving': 'k',
                'westfacing falling': 'l', 'southfacing falling': 'm', 'northfacing falling': 'n', 'box': 'o',
                'northfacing': 'p'}

    if game == 'waferthinmints':
        return {'avatar floor waiter': 'a', 'floor wfm': 'b', 'floor waiter wfm': 'c', 'floor': 'd',
                'floor waiter': 'e', 'wall': 'f', 'avatar floor': 'g'}

    if game == 'waferthinmintsexit':
        return {'floor wfm': 'a', 'floor': 'b', 'floor exit': 'c', 'wall': 'd', 'avatar floor': 'e'}

    if game == 'watergame':
        return {'background': 'a', 'avatar background': 'b', 'background water': 'c', 'background door': 'd',
                'background box': 'e', 'wall': 'f', 'avatar background water': 'g'}

    if game == 'whackamole':
        return {'wall tight slow': 'a', 'wall avatar wide cat': 'b', 'wall wide': 'c', 'wall tight cat': 'd',
                'wall wide quick quick': 'e', 'wall wide quick': 'f', 'wall avatar cat': 'g', 'wall': 'h',
                'wall avatar': 'i', 'wall wide cat': 'j', 'wall avatar wide': 'k', 'wall avatar tight': 'l',
                'wall cat': 'm', 'wall tight': 'n'}

    if game == 'wrapsokoban':
        return {'': 'a', 'avatar hole': 'b', 'hole boxin': 'c', 'avatar box': 'd', 'avatar': 'e', 'hole': 'f',
                'wall': 'g', 'box': 'h'}

    return {x: y for x, y in zip(range(30), range(30))}

