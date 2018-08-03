if __name__ == '__main__':
    with open('version.txt', 'r') as f:
        ver = int(f.readlines()[0].strip())
    with open('deploy.t', 'r', encoding="utf-8") as file:
        script = file.readlines()

    new_tag = 'v0.0.{}'.format(ver)
    print(new_tag)
    script = ''.join(script)
    script = script.replace('$(tag)', new_tag)

    with open('version.txt', 'w') as f:
        f.writelines(str(ver + 1))
    with open('deploy.cmd', 'w', encoding="utf-8") as file:
        file.write(script)
