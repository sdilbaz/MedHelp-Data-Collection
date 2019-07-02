# MedHelp-Data-Collection
Python script for collection of posts and responses in MedHelp

MedHelp website can be used to collect medical questions and conversations in a medical context. The python code supplied here collects the conversations as XML trees which can be used for further processing.

The script first collects the links to communities by visiting forum list page on medhelp. For each forum, all of the links for posts are stored. After the links have been extracted, each post is visited and the post is stored as an XML tree. A sample XML tree extracted through this process is given below.

<div class="highlight highlight-text-xml"><pre>&lt;?<span class="pl-ent">xml</span><span class="pl-e"> version</span>=<span class="pl-s"><span class="pl-pds">"</span>1.0<span class="pl-pds">"</span></span><span class="pl-e"> encoding</span>=<span class="pl-s"><span class="pl-pds">"</span>UTF-8<span class="pl-pds">"</span></span>?&gt;
&lt;<span class="pl-ent">post</span>&gt;
  &lt;<span class="pl-ent">post_fields</span>&gt;
    &lt;<span class="pl-ent">href</span>&gt;https://www.medhelp.org/posts/Diabetes---Gestational/gestational-diabetes-/show/2277904&lt;/<span class="pl-ent">href</span>&gt;
    &lt;<span class="pl-ent">title</span>&gt;gestational diabetes&lt;/<span class="pl-ent">title</span>&gt;
    &lt;<span class="pl-ent">username</span>&gt;TinkerBelly65&lt;/<span class="pl-ent">username</span>&gt;
    &lt;<span class="pl-ent">user_link</span>&gt;/personal_pages/user/7754230&lt;/<span class="pl-ent">user_link</span>&gt;
    &lt;<span class="pl-ent">time</span>&gtThu Aug 21 05:56:50 2014&lt;/<span class="pl-ent">time</span>&gt;
    &lt;<span class="pl-ent">body</span>&gt;Yup so it has happened, less then 9Wks away from my due date and my life is turned upside down. I just found out I've got gestational diabetes. I'm so overwhelmed with all the do's and dont's. Not to mention having to test my blood 4 times a day. So it's day one, I'm starving BUT its only 6am and I still have to go grocery shopping later so hints I have nothing GD friendly to eat. So what do I do?&lt;/<span class="pl-ent">body</span>&gt;
  &lt;/<span class="pl-ent">post_fields</span>&gt;
  &lt;<span class="pl-ent">response</span> <span class="pl-e">resp_id</span>=<span class="pl-s"><span class="pl-pds">"</span>0<span class="pl-pds">"</span></span>&gt;
    &lt;<span class="pl-ent">username</span>&gt;DraevinMark&lt;/<span class="pl-ent">username</span>&gt;
    &lt;<span class="pl-ent">user_link</span>&gt;/personal_pages/user/10055259&lt;/<span class="pl-ent">user_link</span>&gt;
    &lt;<span class="pl-ent">time</span>&gtThu Aug 21 06:21:15 2014&lt;/<span class="pl-ent">time</span>&gt;
    &lt;<span class="pl-ent">body</span>&gt;I have it too and where I come from its hard not to eat the good stuffs. I minimize my starch in take rice etc...drink lots of water. And like u take my blood sugar every day. They're usually below 150's.Good luck I have 58 more days.&lt;/<span class="pl-ent">body</span>&gt;
  &lt;/<span class="pl-ent">response</span>&gt;

&lt;/<span class="pl-ent">post</span>&gt;</pre></div>

The root of the XML tree is contains relevant information from the post such as the link to post, title of the post, username of the poster, link to the poster profile if available, time of posting, and the post body.

If there is a response to the post,  the XML trees will include the responses with information such as the username, the link to the user profile if available, time of posting, and the response body.

Since the python script depends on multiprocessing, it should be used from the command line. The script was written in python3.

Example usage:
	
	python scrape-medhelp.py C:/ --ncpu 3
