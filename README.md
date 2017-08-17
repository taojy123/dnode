# dnode

```

    data = {
        'a': 1,
        'b': {'b1': 3},
        'c': {'c1': 1, 'c2': {'c22': 22}},
        'd': ['d1', 'd2', 'd3'],
        'e': [{'ee': 1}, {'ee': 2}, {'ee': 3}],
        'f': [['f11', 'f12'], ['f21', 'f22']],
        'g': [[{'gg': 11}, {'gg': 12}], [{'gg': 21}, {'gg': 22}]],
    }

    obj = DNode(data)

    print '=========== print object ==============='

    obj.pprint()

    print '============= print json ==============='

    print obj._dumps(4)

    print '=========== test getattr ==============='

    print obj.a
    print obj.b.b1
    print obj.c.c2
    print obj.d[1]
    print obj.e[1].ee
    print obj.f[0][0]
    print obj.g[0][0].gg

    print '=========== test setattr ==============='

    obj.a = 'change_a'
    print obj.a

    obj.b.b1 = 'change_b'
    print obj.b.b1

    obj.c.c2.c22 = 'change_c'
    print obj.c.c2.c22

    obj.d[1] = 'change_d'
    print obj.d[1]

    obj.e[1].ee = 'change_e'
    print obj.e[1].ee

    obj.f[0][0] = 'change_f'
    print obj.f[0][0]

    obj.g[0][0].gg = 'change_g'
    print obj.g[0][0].gg

    print '============== test clear ==============='

    obj.clear()

    obj.pprint()

    print '========================================='
    
```
