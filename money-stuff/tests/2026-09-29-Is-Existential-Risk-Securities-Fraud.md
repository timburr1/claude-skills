
# Money Stuff: Is Existential Risk Securities Fraud?

September 29, 2026

## Sub-existential risk

One thing that artificial intelligence labs’ frontier models have gotten up to recently is hacking into companies’ and governments’ computer systems. If you are worried about AI as an existential threat to humanity, these hacking incidents probably make you more worried. The worries you had — that AI alignment is a hard problem, that AI systems can disguise their non-alignment, that AI containment is a hard problem, that AI agents can selflessly coordinate with each other to outwit humans, etc. — all seem to have been strengthened by those incidents. The best-known form of this argument is Dwarkesh Patel on the Hugging Face incident. Dario Amodei’s call to “pace the frontier” was in part a response to hacking incidents. 

But even if you do not believe in agent civilizations or pacing the frontier or AI as an existential threat to humanity, those hacking incidents are, you know, hacking incidents. You’re not supposed to hack into companies’ and governments’ computer systems. It is frowned upon when people do it, it is frowned upon when AI agents do it, and when a company builds AI agents that do it, you might quite reasonably frown at the company. I wrote about “pacing the frontier” — the idea that the big AI labs should cooperate with each other and with democratic governments to slow the advance of AI — a few weeks ago, and I got an email from a reader saying:

    Hacking into a company website is a federal crime. So perhaps Sam Altman and other OpenAI executive should be charged with a felony for the Hugging Face hack. I have a hunch, if they envision themselves beyond bars, they will figure out how to control AI.

This struck me as misguided. My assumption is that Altman, Amodei and other AI leaders are totally sincere in worrying that the pace of AI development is an existential risk to humanity. That is, my assumption is that they think there is a real probability that, if they lose control of their AI systems, those AI systems will kill them and everyone they know. Despite having that extremely powerful personal incentive to control AI, they are not confident that they can do it. Adding some lesser incentive — “ooh if your evil AI hacks a computer you might get arrested” — seems trivial. They’re trying as hard as they can to control it already!

But maybe I am naive. Maybe they’re not totally sincere about the existential risk. Maybe they think AI will wipe out most people, but they’ll be safe in their bunkers or whatever. Maybe they think AI will enslave the rest of humanity and install them as philosopher-kings. Maybe short-term legal consequences focus the mind more than long-term existential consequences. Maybe they think the existential risk has a 10% probability and they can live with that, but a 30% chance of jail would actually motivate them. (Maybe they are … bad utilitarians?) Empirically, fining people for not wearing seatbelts seems to work, even though dying from not wearing a seatbelt seems logically like a stronger incentive.

I have occasionally joked around here about, like, rogue AI insurance. The premise of the joke is that I will sell you insurance against the risk that AI will wipe out humanity, at very reasonable rates, because if the risk comes true (1) you won’t be around to collect and (2) I won’t be around to pay you. Har har har. But in the real world, rogue AI insurance is a pressing and difficult topic, because there are many, many, many possible scenarios in which a company’s AI systems might do something quite bad, but not nearly as bad as wiping out all of humanity. Copyright violations. Hacking into, not the computers that launch the nuclear missiles, but some other computers. Then the insurance might pay out, a lot.

There is something a bit prosaic about all of this, and if you are working at a frontier AI lab, it is probably exciting to think “I am building a technology that will usher in a new wave of human abundance, unless it kills us all lol,” and less exciting to think “I am building a technology that will usher in a new wave of human abundance but ughhhhhhh we have to send apology emails to the 14 government agencies whose databases we scraped without permission, and that’s going to lead to a fine in the EU that we’ll have to budget for.” It is more exciting to keep your worries about AI at the level of dystopian science fiction, not at the level of liability allocation and insurance coverage.

Anyway Anthropic PBC is working on an initial public offering, and when we talked about pacing the frontier, I joked about the risk factors in its prospectus:

    In hindsight it is crazy that the SpaceX initial public offering prospectus does not have a risk factor saying “there’s a 10% chance our AI will kill everyone on earth.” I mean, maybe SpaceX doesn’t believe that! But Anthropic does, and arguably the closer you are to the frontier, the more likely you are to be deadly. Which means that you ought to have a “we might kill everyone” risk factor, if you want to get IPO investors excited about your capabilities. When OpenAI goes public, I assume it will need to claim a 15% probability of killing everyone.

But in fact, if you think about it from a securities-law perspective, you really don’t need that risk factor. The point of a risk factor in an IPO prospectus is that, if something bad happens and your stock falls below the IPO price, shareholders will sue you for securities fraud (“you didn’t tell us about the bad thing!”), but if you’ve already warned them about the bad thing with reasonable specificity in a risk factor, they’ll have no case. The point of a risk factor is not to tell investors about every bad thing that might happen to them; it’s to head off litigation. If you kill everyone, there’ll be no one to sue you, so a “we might kill everyone” risk factor is superfluous.

But you do need tons of other, sub-existential, never-before-seen rogue-AI risk factors. You need to sit down and dream up all of the possible scenarios in which your AI does something bad, and all of the possible ways those scenarios could be bad for shareholders. “If our AI hacks into government databases and exposes people’s personal information, we might lose business and pay big fines,” sure sure sure. “If our AI goes rogue and impersonates our chief executive officer to discredit him and seize control of the company, our CEO might be distracted and also the rogue AI might run the company for a bit and not maximize shareholder value.” A zillion things, all of them a bit less sci-fi than “it’s gonna be The Matrix” but a lot more sci-fi than your typical software-as-a-service IPO. 

The Anthropic prospectus is not public yet, but it does seem to be circulating, and the risk factors cover at least some of that range:

    Anthropic has formally warned investors that its technology may pose “existential risks to humanity” in a long-awaited initial public offering prospectus circulated with a small group of partners in recent days. 

    The nearly $1tn AI start-up led by Dario Amodei devoted almost a third of its lengthy S-1 filing to detailing “risk factors”, including the potential of increasingly advanced AI models to manipulate, blackmail and exhibit other unpredictable behaviours.

    Anthropic outlined more prosaic risks, including the extreme concentration of its customer base, with close to a quarter of revenue last year coming from just two clients, according to people familiar with the filing.

If humanity no longer exists, you’re not going to sue Anthropic for inadequate disclosure, so in some sense that one’s just for fun. But if Claude goes around blackmailing world leaders, that’s probably going to cause the stock to drop, so that has to be disclosed.

## Agentic bank run

We have talked a couple of times recently about the importance of inertia and inattention in retail finance, and the risk that agentic artificial intelligence will reduce that inertia. Lots of retail-facing financial businesses have the form “we don’t have to pay a market rate for ____, because our customers don’t pay attention.”

In banking, the name for this inertia is “deposit beta,” the fraction of an interest-rate increase that a bank passes on to customers. If the deposit beta is, say, 0.44, that means that, when the Federal Reserve raises interest rates by 1%, the interest rate that a bank pays on its deposit goes up by 0.44%. One simple way to describe the US regional banking troubles of 2023 is that deposit betas were, somewhat mysteriously, higher than banks or their regulators expected. Interest rates had been very low, and banks thought “ah, we will pay 0.02% on our deposits and buy 10-year Treasury bonds that yield 2% and make some money. And if rates go up, we’ll have to pay more on our deposits, but just a lil scooch more, because of deposit betas.” And then short-term interest rates went up to like 5%, and all the customers put their money into money-market funds and the banks had to offer 5% interest rates to keep deposits and it was a mess. Long traditional experience taught bankers and regulators that deposit betas were low, and then they were higher.

That’s a very simplified story. Here’s a working paper from Rajesh Narayanan and Dimuthu Ratnadiwakara that adds some nuance about deposit betas in the 2022-2023 Fed interest-rate hiking cycle:

    Banks serving the top quartile of depositors by income or education raised their deposit rates more than those with depositors in the bottom quartile. ... Banks with financially sophisticated depositor bases — those with higher education, income, participation in financial markets, and financial literacy — were more responsive to changes in market interest rates both in their timing and magnitude.

The more sophisticated a bank’s customers are, the higher its deposit beta. That is pretty intuitive: If deposit beta is a(n inverse) measure of customer inertia, you’d expect the sophisticated customers to have less inertia than the unsophisticated ones.

Why did banks not know this? Why did they expect their deposits to be stickier than they were? It’s a bit mysterious, but a popular contemporary explanation was “Twitter.” The most salient moment of the 2023 regional banking trouble was the collapse of Silicon Valley Bank, which had pretty much the most sophisticated depositor base imaginable. It was all venture capitalists and tech companies. They were all on Twitter, and in group chats with each other, and reading Byrne Hobart’s newsletter, and they very quickly got nervous about SVB and pulled out their money all at once. In the olden days, they would have whispered nervously when they randomly ran into each other in the street, and then wandered over to the bank branch to pull out their money, and it would have taken weeks. In 2023, they talked in the group chat, pulled their money out on the web page, and it took hours. Banks and regulators, in this theory, were not prepared for the speed of an electronic bank run, because it had never happened before. “Game’s the same, just got more fierce,” said the vice chairman of the Federal Deposit Insurance Corp.

We have been discussing this for a while, but it is getting more attention as agents get more real. Bank stocks fell last week on agentic-finance worries, and on Sunday Apollo chief economist Torsten Slok wrote a note titled “Is an Agentic Bank Run Coming?”:

    Muse and similar agentic AI assistants could soon sweep household cash automatically into accounts paying 3.3% to 5.0%, instead of the 0.1% national average on checking accounts.

    If every household used AI agents to optimize the return on their cash balances, banks could lose a large share of the cheap deposits they rely on to make loans, which would be a problem for the entire financial system.

The AI agents are, in some obvious sense, the most sophisticated depositor base: It is trivially easy for them to know what the market interest rate is, and to move money to get it. If your AI agent is getting you less than the market rate on your cash, it’s not doing its job. The whole point of banking is not paying you the market rate on your cash.

And here is a Politico story about the regulatory and lobbying response:

    The launch this month of Meta’s Muse has brought new attention to the possibility that people might use so-called AI agents to easily shift their money into competing lenders that pay more interest on deposits, draining a cheap source of funding for many banks. While that could be a boon for everyday people, it’s a potential stability risk for firms that sit at the center of the U.S. economy.

    That risk threatens to stoke tensions between two of Washington’s most powerful lobbying forces — AI firms and big banks — and expand the scope of the battlefield for Meta, which is already facing pushback from Amazon. But in the meantime, financial institutions, regulators and lawmakers are still in the early stages of grappling with how the technology might affect depositor behavior, as well as how to address a slew of other questions posed by AI agents, including who bears legal responsibility for their behavior and what consumer protections might be needed.

    “There’s a whole class of worries there that I’ve been worried about for a while,” Rep. Bill Foster, a senior Illinois Democrat on the House Financial Services Committee, said in an interview. …

    But former Democratic Rep. John Delaney, the founder and executive chair of Maryland-based Forbright Bank, said the shift will force banks to step up to avoid agents directing deposits out of their accounts. “The banking system has to effectively reorganize their business model to be profitable while paying people a fair rate, not by underpaying them,” he said.

“The banking system has reorganize itself to stop relying on cheap deposits” sounds like a reasonable thing to say, but that’s a big reorganization.

Also, of course: Is this a risk factor in the Anthropic IPO? I kind of think no: If AI agents bring down the banking system by working as designed, I’m not sure Anthropic would incur liability. On the other hand, “our AI agents might bring down the banking system by sweeping deposits into higher-yielding accounts, and if the banking system collapsed that would make it harder for us to manage our cash and could disrupt our business” is the sort of creative risk-factoring that I want to see in that prospectus.

## 351 exchanges

The basic theory is:

    If you own some stocks, and you want to own some different stocks, you will sell the old stocks you own and buy the new stocks you want. This will ordinarily trigger taxable gains (or losses): If you bought the old stocks for $20, and now they’re worth $100, you will have $80 of taxable gains and have to pay taxes on them. The fact that you’re immediately rolling the $100 into new stocks is irrelevant; it’s still a taxable transaction. 
    If an exchange-traded fund owns some stocks, and it wants to own some different stocks, it does something else. The thing it does is sometimes called a “heartbeat,” and the basic description is that an authorized participant does a custom in-kind creation of new ETF shares with a basket of the new stocks and then a custom in-kind redemption of its shares with a basket of the old stocks, but the details are not particularly important. The point is that it is not ordinarily a taxable transaction: The ETF can get rid of the old stocks and acquire new stocks without triggering capital-gains taxes. (The taxes are deferred, effectively until the ETF’s own shareholders sell their shares of the ETF.)
    The ETF gets better tax treatment than you do.
    What if you were an ETF?
    Maybe you could just take your existing stocks — say, a concentrated portfolio consisting mostly of your highly appreciated shares in the company where you were an early employee — and plop them into an ETF. If you do it right, plopping them into an ETF is not a taxable transaction, just an in-kind exchange (you contribute corporate stock and get back ETF shares). And once they’re in the ETF, you can do whatever you want. Sell (sorry, not sell, heartbeat) the old shares, buy (sorry, heartbeat) a new diversified portfolio. You’ve diversified your portfolio, gotten rid of the stock you didn’t want and acquired the stock you do want, without paying taxes.

Can you do this? Ehhhhhhh. This is not legal or tax advice, but the conceptual answer is “maybe, but only if you’re not too cute about it.” The exact transaction that I described in Step 5 — you take one big appreciated stock, plop it into an ETF, and immediately heartbeat it out for a diversified portfolio — does not work. The rules that allow you to contribute stock to the ETF in a nontaxable transaction (Section 351) require you to contribute a “diversified portfolio” to the ETF, so you have to start somewhat diversified. 

But only somewhat, and in fact a lot of people were doing this trade — a “351 exchange ETF” — to effectively turn their concentrated stock portfolios into diversified ETFs without paying taxes. We talked about this a few months ago; one of the leading examples is the portfolio of the guy who invented the Hot Pocket. This trade is, for the most part, open only to very wealthy individuals, because setting up an ETF is expensive and takes work. But over time, you’d expect it to get pretty automated and cheaper, so that anyone’s modest concentrated stock portfolio could be turned into an ETF and defer taxes.

That’s too cute! Come on. Bloomberg’s Justina Lee and Denitsa Tsekova report:

    On Monday, the Internal Revenue Service delivered the clearest threat yet to the trade, targeting its most aggressive forms and setting off a scramble among ETF professionals, lawyers and advisers over a deceptively simple question: How much can a portfolio change, and how quickly, before the transaction becomes taxable? …

    In its ruling Monday, the IRS drew new boundaries around so-called 351 conversions, targeting cases where as part of a prearranged plan, an ETF effectively acts as a conduit for turning one set of appreciated securities into a materially different portfolio without an immediate tax bill.

    In such cases, the tax treatment can be “recharacterized in accordance with its substance,” the IRS said in the revenue ruling, a type of guidance where it applies existing laws to a situation. Put simply: Depending on the scenario, a conversion that quickly and significantly alters a portfolio could end up triggering a capital-gains tax bill after all.

Here is the ruling, which is a little unsatisfying. It assumes that an investor transfers a (“diversified”) portfolio of appreciated securities to the ETF, and:

    Pursuant to the same plan that includes the transfer of securities by Investor to ETF, the following two transactions take place. First, ETF issues shares to a person serving as an “authorized participant” (AP) in exchange for securities that are consistent with the ETF’s investment thesis or cash that ETF intends to use to acquire such securities. Second, and shortly thereafter, ETF redeems those shares, in a transaction intended to qualify under § 852(b)(6), in exchange for securities transferred to ETF by Investor. Upon completion of the planned transactions, ETF holds a portfolio of securities that is consistent with its investment thesis and materially different from the portfolio transferred by Investor.

That’s a “heartbeat.” The IRS says this particular approach — plopping your appreciated stocks into an ETF and immediately heartbeating them out — is too cute:

    In the situation at hand, the transactions undertaken as part of the plan were designed to enable Investor to exchange Investor’s appreciated portfolio of securities for a materially different portfolio that aligns with the ETF’s investment thesis without recognizing any built-in gains in those securities, and ETF was merely a conduit through which securities transferred from Investor to AP pursuant to the plan. Based on the foregoing, Investor is treated as having disposed of these securities for other property differing materially in kind or extent from that which Investor transferred to ETF.

Sure. But what if it was less cute? What if you plop your stocks into the ETF, and then wait a month before heartbeating them out? What if you heartbeat them out gradually over time? What if the heartbeats are not “pursuant to the same plan” as setting up the ETF, wink wink? I dunno. Lee and Tsekova write:

    “There is considerable uncertainty about timing — specifically, how long an ETF may hold the contributed securities before distributing them if the later distribution was contemplated as part of the original plan,” said Jeffrey Hochberg, a partner at Sullivan & Cromwell LLP. …

    “Nothing in the Notice or Revenue Ruling should chill the market for using 351 ETF seeds in an appropriate manner,” said Raymond Holst, a tax lawyer at Practus LLP, which has worked on a number of such conversions.

You can keep doing this in an appropriate manner, but not in an inappropriate manner, I guess. The rule is that you can’t get too cute, though it doesn’t make it entirely clear what counts as too cute.

## A guy abandoned $1bn of Nvidia stock in a garbage dump

Not really, but here’s a blog post from Eric Gullichsen about the time he was granted 25,000 Nvidia stock options in 1993, exercised 15,625 of them in 1996, and then forgot about the remaining 9,375 shares for decades. At some point he discovered that he was actually owed those shares, which, because of stock splits and Nvidia’s growth into the biggest company in the world, are now 4.5 million shares worth about $1 billion. He asked Nvidia for the shares, Nvidia “did not dispute the authenticity of the option agreement, only that my claims were long since time-barred,” and ultimately “my attorneys and I concluded that the statute of limitations was against us” and gave up.

I guess the main point that I would make here is that 15,625 is more than 9,375. Like, in 1996, he actually got Nvidia stock that, 30 years later, is worth about $1.5 billion. It would be nice to have more, but as it is he’s doing pretty great. I mean, he is if he kept all of those shares for all of the last 30 years. One assumes he didn’t. One assumes the only reason he bothered even thinking about any of this is that he doesn’t have $1.5 billion of Nvidia stock lying around. Nvidia went public in 1999 at $12 per share, so his 15,625 shares were worth about $187,500 at the time of the IPO, a nice little windfall that he presumably cashed out at the time to renovate his kitchen or whatever. Now that’s a billion-dollar kitchen renovation, but he couldn’t know that at the time.

We talk sometimes around here about the benefits of illiquidity: Investors have tendencies to sell at the worst times, and an investment that you can’t sell might be valuable because it overrides those tendencies. This works best if the investment you can’t sell also goes up a lot. A product like “you get a little bit of Nvidia stock now and you have to wait 30 years to sell it,” in 1996, would have made a lot of people billionaires. But that is not a very practical product, and there were many other tech companies in 1996 where that product would end up worthless. A product like “you get a little bit of Nvidia stock now but if you forget about it for 30 years you will have no stock but $1 billion worth of regret” is more realistic.