using LogAnalysis.Data;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.Extensions.FileProviders;
using System.Text.Encodings.Web;

var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseKestrel(options =>
{
    options.Limits.MaxConcurrentConnections = 100;
    options.Limits.KeepAliveTimeout = TimeSpan.FromSeconds(600);
});

// Add services to the container.
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
builder.Services.AddSingleton<WeatherForecastService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
}


app.UseStaticFiles();

var dir = Path.Combine(app.Environment.WebRootPath, "Upload");
if (!Directory.Exists(dir)) Directory.CreateDirectory(dir);

var opt = new DirectoryBrowserOptions
{
    FileProvider = new PhysicalFileProvider(dir),
    Formatter = new AME.HtmlDirectoryFormatterChsSorted(HtmlEncoder.Default),
    RequestPath = new PathString("/Upload")
};
app.UseDirectoryBrowser(opt);

app.UseRouting();

app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
