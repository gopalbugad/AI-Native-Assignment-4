
local CustomHandler = {
  VERSION = "1.0.0",
  PRIORITY = 1000
}

function CustomHandler:access(conf)
  local ip = kong.client.get_ip()
  local method = kong.request.get_method()
  local path = kong.request.get_path()

  kong.service.request.set_header("X-Custom-Processed", "true")

  kong.log.notice("StructuredLog | IP:", ip,
                  " | Method:", method,
                  " | Path:", path)
end

return CustomHandler
