"""
1, 2, 3,
=> { count: 3, seq: [1, 2, 3]}


{ "a": 1 }
{ "b": 2 }
=> { count: 2, seq: [{ "a": 1 }, { "b": 2 }]}


{ "a" : 
1,
"b":
2
}
=> { count: 1, seq: [{{ "a" : 1 }}]}


{"a":3} 5{"cool":       8}"string"
=> { count: 4, seq: [{"a": 3}, 5, {"cool": 8}, "string]}

1   2   3
=> { count: 3, seq: [1, 2, 3]}


1
2
3
=> { count: 3, seq: [1, 2, 3]}

1         2         3
=> { count: 3, seq: [1, 2, 3]}

123 456
=> { count: 2, seq: [123, 456]}
















"""
