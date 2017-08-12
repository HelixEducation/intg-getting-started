Sample project for getting up and running quicker with Application Integration

# Setup
This library leverages the default AWS credentials that are set within the .Net configuration. You can set these via the AWS PowerShell Toolkit:
```
PS C:\> Install-Package -Name AWSPowerShell
```

And then install the credentials via:
```
PS C:\> Set-AWSCredential -AccessKey {accesskey} -SecretKey {secretkey} -StoreAs {profileordefault}
```

See the [Setting up the AWS Tools for Windows PowerShell Amazon article](http://docs.aws.amazon.com/powershell/latest/userguide/pstools-getting-set-up.html) for more information.

# Building and Running
Packages are bundled, but can be [reinstalled with NuGet](https://docs.microsoft.com/en-us/nuget/consume-packages/reinstalling-and-updating-packages) if necessary.

The sample project runs as a console application (after Build -> Run).
