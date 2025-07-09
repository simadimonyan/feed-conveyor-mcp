from mcp.server.fastmcp import FastMCP

web = FastMCP("web", host="0.0.0.0", port=8082)
analytics = FastMCP("analytics", host="0.0.0.0", port=8082)

if __name__ == "__main__":
    web.run(transport="sse")