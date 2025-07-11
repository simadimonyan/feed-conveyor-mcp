from mcp.server.fastmcp import FastMCP
from tools.web_server import WebTools

web = FastMCP("web", host="0.0.0.0", port=8082)
analytics = FastMCP("analytics", host="0.0.0.0", port=8082)

WebTools(web)

if __name__ == "__main__":
    web.run(transport="sse")