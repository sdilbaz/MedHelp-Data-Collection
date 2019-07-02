# MedHelp-Data-Collection
Python script for collection of posts and responses in MedHelp

MedHelp website can be used to collect medical questions and conversations in a medical context. The python code supplied here collects the conversations as XML trees which can be used for further processing.

The script first collects the links to communities by visiting forum list page on medhelp. For each forum, all of the links for posts are stored. After the links have been extracted, each post is visited and the post is stored as an XML tree. A sample XML tree extracted through this process is given below.

-<post>


-<post_fields>

<href>https://www.medhelp.org/posts/Diabetes---Gestational/gestational-diabetes-/show/2277904</href>

<title>gestational diabetes</title>

<username>TinkerBelly65</username>

<user_link>/personal_pages/user/7754230</user_link>

<time>Thu Aug 21 05:56:50 2014</time>

<body>Yup so it has happened, less then 9Wks away from my due date and my life is turned upside down. I just found out I've got gestational diabetes. I'm so overwhelmed with all the do's and dont's. Not to mention having to test my blood 4 times a day. So it's day one, I'm starving BUT its only 6am and I still have to go grocery shopping later so hints I have nothing GD friendly to eat. So what do I do?</body>

</post_fields>


-<response resp_id="0">

<username>DraevinMark</username>

<user_link>/personal_pages/user/10055259</user_link>

<time>Thu Aug 21 06:21:15 2014</time>

<body>I have it too and where I come from its hard not to eat the good stuffs. I minimize my starch in take rice etc...drink lots of water. And like u take my blood sugar every day. They're usually below 150's.Good luck I have 58 more days.</body>

</response>

</post>

The root of the XML tree is contains relevant information from the post such as the link to post, title of the post, username of the poster, link to the poster profile if available, time of posting, and the post body.

If there is a response to the post,  the XML trees will include the responses with information such as the username, the link to the user profile if available, time of posting, and the response body.

