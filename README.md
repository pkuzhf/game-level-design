# game-level-design

## simulator.py
A demo of this simulator is following:

```python
import simulator

cache=simulator.cache(lambda *vartuple:1);

players=[
    '5be824d7877e066ded50b599',
    '5be66437a421b05c5cfc08db',
    '5be833ed877e066ded50bce6',
    '5be65729a421b05c5cfc043c',
    '5bdd9678e5446d17d00b06e9',
    '5be66298a421b05c5cfc0841',
    '5be66151a421b05c5cfc07a3',
    '5be0532ce5446d17d00ce073'
    ]

player0=players[0]
player1=players[1]
initData=[74600491, 31718972, 111170161]
    
nCase=5

for i in range(nCase):
    result,cur,ave,counter,total=cache.run(player0,player1,initData)
    print("Case #%d:"%(i))
    print("player0: %s"%(player0))
    print("player1: %s"%(player0))
    print("result: ",result.json())
    print("current score: %f"%(cur))
    print("average score: %f"%(ave))
    print("counter: %d"%(counter))
    print("total: %d"%(total))
    print("===================================================================")


```

