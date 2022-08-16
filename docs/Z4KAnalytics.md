# Z4K Analytics

Z4K Analytics is available through Zerto Analytics.

Access Zerto Analytics from one of the following locations:

  *	From a URL: https://analytics.zerto.com
  * From myZerto: www.zerto.com/myzerto. Sign in using your credentials and select the Analytics tab.

Z4K Analytics currently supports the following tabs:

1. Dashboard
2. VPGs
3. Monitoring

Z4K analytics transmission is set to True by default and is tweakable by using the values True or False:

For example if you wish to stop Z4K analytics transmission use the following command from CLI:
```
$ kubectl zrt set-tweak EnableZertoAnalyticsTransmitter False
```

For more info about Zerto Analytics see [Zerto Analytics - Overview and Use](https://help.zerto.com/bundle/Zerto.Analytics.HTML/page/Content/Zerto_Analytics/Zerto_Analytics_-_Overview_and_Use.htm)
