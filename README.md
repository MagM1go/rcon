# rcon
A simple RCON controller

```python
rcon = RCON("localhost", 22575, "mypswd")

async with rcon as connection:
    await connection.connect_to_rcon()
    output = await connection.execute_command("troll")
    
print(output)
```
