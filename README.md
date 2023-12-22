# rcon
A simple RCON controller

```python
rcon = RCON()

async with rcon as connection:
    await connection.connect_to_rcon("localhost", 22575, "mypswd")
    output = await connection.execute_command("troll")
    
print(output)
```
