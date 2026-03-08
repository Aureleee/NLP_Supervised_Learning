*This project has been created by ...*
## NLP Project Description
This repo is meant to describe our code and explain the choices we made, i hope you'll enjoy it :D.
___
### NLP Idea
Here we need to complet this, gniark, gniark  ```.txt``` 
- We can do things like this : *This is cool*

Bla Bla Bla 

---
## Instruction
*Let's assume you know nothing about git or coding ig haha. Just follow this steps to begins wiht :D*
```bash
git clone git@github.com:Aureleee/NLP_Supervised_Learning.git potato
``` 
```bash
cd potato
```
&rarr; You can now see our project hhe 

# NEXT IS AN EXAMPLE OF CODE INSIGHT WE CAN SHOW (Here its for GNL)

### Code insight

As an example let's say file.txt = `Hello\nI\nlike\napple`
Considering you know smt about fd, we will use `BUFFER_SIZE = 4` and see steps by steps how our code is doing.

```c
if (fd < 0 || BUFFER_SIZE <= 0)
        return (NULL);
    buffer = malloc(BUFFER_SIZE + 1);
    bytes_read = 1;
```

At this point:

```c
buffer = { ? , ? , ? , ? , ? }
stash = (null)
```

Hence we go into the loop:

```c
while (!ft_strchr(stash, '\n') && bytes_read != 0)
// stash is null -> !ft_strchr(stash, '\n') is true 
    {
        bytes_read = read(fd, buffer, BUFFER_SIZE);
        // buffer = { 'H', 'e', 'l', 'l', '\0' }
        
        if (bytes_read == -1)
        {
            free(buffer);
            return (NULL);
        }
        buffer[bytes_read] = '\0';
        stash = ft_strjoin(stash, buffer);
        // now stash = "Hell"
    }
```

After the first `read`, your memory looks like this:
```c
buffer = { 'H', 'e', 'l', 'l', '\0' }
stash  = "Hell" // After ft_strjoin
```

Since `stash` does NOT contain `\n`, the loop continues.


```c
bytes_read = read(fd, buffer, BUFFER_SIZE); 
// buffer now gets: { 'o', '\n', 'I', '\n', '\0' }
stash = ft_strjoin("Hell", "o\nI\n");
```
```c
stash = { 'H' , 'e' , 'l' , 'l' , 'o' , '\n' , 'I' , '\n'}
```

The loop stops here because `ft_strchr(stash, '\n')` is ```True```

Now we call `line = ft_extract_line(stash);`

```c
// It scans stash until the first '\n'
line = { 'H', 'e', 'l', 'l', 'o', '\n', '\0' }
```


Now we must save the rest for the next call of `get_next_line`.
We call `stash = ft_clean_stash(stash);`

```c
// stash + i + 1 points to the character after the first '\n'
stash = { 'I', '\n', '\0' } 
```

### Final State of the first call

* **Return:** `line` ("Hello\n") is sent to the user.
* **Persistence:** `stash` ("I\n") stays in memory because it's **static**.
* **Memory:** `buffer` is freed.

---

When you call `get_next_line` again:

1. The `while` condition checks `ft_strchr(stash, '\n')`.
2. **Surprise!** There is already a `\n` in "I\n".
3. The loop is skipped entirely.
4. `ft_extract_line` picks up "I\n".
5. `stash` becomes `NULL`.

---
### Resource 
---
I almost asked any question i had to [ChatGPT](https://chatgpt.com/), sometimes i went to see what my friend did, but most of it come from me. And each time i faced an issue, ChatGPT got my back hahah

Anyway  i also used the [GNU C Reference Manual](https://www.justice.gov/epstein/files/DataSet%209/EFTA00315849.pdf)
 