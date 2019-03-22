import tempfile
from integration.testcase import CommandTestCase


class EpicAdventuresOfChris45(CommandTestCase):

    async def test_no_this_is_not_a_test_its_an_adventure(self):
        # Chris45 is an avid user of LBRY and this is his story. It's fact and fiction
        # and everything in between; it's also the setting of some record setting
        # integration tests.

        # Chris45 starts everyday by checking his balance.
        result = await self.daemon.jsonrpc_account_balance()
        self.assertEqual(result, '10.0')
        # "10 LBC, yippy! I can do a lot with that.", he thinks to himself,
        # enthusiastically. But he is hungry so he goes into the kitchen
        # to make himself a spamdwich.

        # While making the spamdwich he wonders... has anyone on LBRY
        # registered the @spam channel yet? "I should do that!" he
        # exclaims and goes back to his computer to do just that!
        channel = await self.out(self.daemon.jsonrpc_channel_new('@spam', "1.0"))
        self.assertTrue(channel['success'])
        await self.confirm_tx(channel['tx']['txid'])

        # Do we have it locally?
        channels = await self.out(self.daemon.jsonrpc_channel_list())
        self.assertEqual(len(channels), 1)
        self.assertEqual(channels[0]['name'], '@spam')

        # As the new channel claim travels through the intertubes and makes its
        # way into the mempool and then a block and then into the claimtrie,
        # Chris doesn't sit idly by: he checks his balance!

        result = await self.daemon.jsonrpc_account_balance()
        self.assertEqual(result, '8.989893')

        # He waits for 6 more blocks (confirmations) to make sure the balance has been settled.
        await self.generate(6)
        result = await self.daemon.jsonrpc_account_balance(confirmations=6)
        self.assertEqual(result, '8.989893')

        # And is the channel resolvable and empty?
        response = await self.out(self.daemon.jsonrpc_resolve('lbry://@spam'))
        self.assertIn('lbry://@spam', response)
        self.assertIn('certificate', response['lbry://@spam'])

        # "What goes well with spam?" ponders Chris...
        # "A hovercraft with eels!" he exclaims.
        # "That's what goes great with spam!" he further confirms.

        # And so, many hours later, Chris is finished writing his epic story
        # about eels driving a hovercraft across the wetlands while eating spam
        # and decides it's time to publish it to the @spam channel.
        with tempfile.NamedTemporaryFile() as file:
            file.write(b'blah blah blah...')
            file.write(b'[insert long story about eels driving hovercraft]')
            file.write(b'yada yada yada!')
            file.write(b'the end')
            file.flush()
            claim1 = await self.out(self.daemon.jsonrpc_publish(
                'hovercraft', '1.0', file_path=file.name, channel_id=channel['claim_id']
            ))
            self.assertTrue(claim1['success'])
            await self.confirm_tx(claim1['tx']['txid'])

        # He quickly checks the unconfirmed balance to make sure everything looks
        # correct.
        result = await self.daemon.jsonrpc_account_balance()
        self.assertEqual(result, '7.969786')

        # Also checks that his new story can be found on the blockchain before
        # giving the link to all his friends.
        response = await self.out(self.daemon.jsonrpc_resolve('lbry://@spam/hovercraft'))
        self.assertIn('lbry://@spam/hovercraft', response)
        self.assertIn('claim', response['lbry://@spam/hovercraft'])

        # He goes to tell everyone about it and in the meantime 5 blocks are confirmed.
        await self.generate(5)
        # When he comes back he verifies the confirmed balance.
        result = await self.daemon.jsonrpc_account_balance()
        self.assertEqual(result, '7.969786')

        # As people start reading his story they discover some typos and notify
        # Chris who explains in despair "Oh! Noooooos!" but then remembers
        # "No big deal! I can update my claim." And so he updates his claim.
        with tempfile.NamedTemporaryFile() as file:
            file.write(b'blah blah blah...')
            file.write(b'[typo fixing sounds being made]')
            file.write(b'yada yada yada!')
            file.flush()
            claim2 = await self.out(self.daemon.jsonrpc_publish(
                'hovercraft', '1.0', file_path=file.name, channel_name='@spam'
            ))
            self.assertTrue(claim2['success'])
            self.assertEqual(claim2['claim_id'], claim1['claim_id'])
            await self.confirm_tx(claim2['tx']['txid'])

        # After some soul searching Chris decides that his story needs more
        # heart and a better ending. He takes down the story and begins the rewrite.
        abandon = await self.out(self.daemon.jsonrpc_claim_abandon(claim1['claim_id'], blocking=False))
        self.assertTrue(abandon['success'])
        await self.confirm_tx(abandon['tx']['txid'])

        # And now checks that the claim doesn't resolve anymore.
        response = await self.out(self.daemon.jsonrpc_resolve('lbry://@spam/hovercraft'))
        self.assertNotIn('claim', response['lbry://@spam/hovercraft'])

        # After abandoning he just waits for his LBCs to be returned to his account
        await self.generate(5)
        result = await self.daemon.jsonrpc_account_balance()
        self.assertEqual(result, '8.969381')

        # Amidst all this Chris receives a call from his friend Ramsey
        # who says that it is of utmost urgency that Chris transfer him
        # 1 LBC to which Chris readily obliges
        ramsey_account_id = (await self.daemon.jsonrpc_account_create("Ramsey"))['id']
        ramsey_account = self.daemon.get_account_or_error(ramsey_account_id)
        ramsey_address = await self.daemon.jsonrpc_address_unused(ramsey_account_id)
        result = await self.out(self.daemon.jsonrpc_wallet_send('1.0', ramsey_address))
        self.assertIn("txid", result)
        await self.confirm_tx(result['txid'])

        # Chris then eagerly waits for 6 confirmations to check his balance and then calls Ramsey to verify whether
        # he received it or not
        await self.generate(5)
        result = await self.daemon.jsonrpc_account_balance()
        # Chris' balance was correct
        self.assertEqual(result, '7.969257')

        # Ramsey too assured him that he had received the 1 LBC and thanks him
        result = await self.daemon.jsonrpc_account_balance(ramsey_account_id)
        self.assertEqual(result, '1.0')

        # After Chris is done with all the "helping other people" stuff he decides that it's time to
        # write a new story and publish it to lbry. All he needed was a fresh start and he came up with:
        with tempfile.NamedTemporaryFile() as file:
            file.write(b'Amazingly Original First Line')
            file.write(b'Super plot for the grand novel')
            file.write(b'Totally un-cliched ending')
            file.write(b'**Audience Gasps**')
            file.flush()
            claim3 = await self.out(self.daemon.jsonrpc_publish(
                'fresh-start', '1.0', file_path=file.name, channel_name='@spam'
            ))
            self.assertTrue(claim3['success'])
            await self.confirm_tx(claim3['tx']['txid'])

        await self.generate(5)

        # He gives the link of his story to all his friends and hopes that this is the much needed break for him
        uri = 'lbry://@spam/fresh-start'

        # And voila, and bravo and encore! His Best Friend Ramsey read the story and immediately knew this was a hit
        # Now to keep this claim winning on the lbry blockchain he immediately supports the claim
        tx = await self.out(self.daemon.jsonrpc_claim_new_support(
            'fresh-start', claim3['claim_id'], '0.2', account_id=ramsey_account_id
        ))
        await self.confirm_tx(tx['txid'])

        # And check if his support showed up
        resolve_result = await self.out(self.daemon.jsonrpc_resolve(uri))
        # It obviously did! Because, blockchain baby \O/
        self.assertEqual(resolve_result[uri]['claim']['amount'], '1.0')
        self.assertEqual(resolve_result[uri]['claim']['effective_amount'], '1.2')
        self.assertEqual(resolve_result[uri]['claim']['supports'][0]['amount'], '0.2')
        self.assertEqual(resolve_result[uri]['claim']['supports'][0]['txid'], tx['txid'])
        await self.generate(5)

        # Now he also wanted to support the original creator of the Award Winning Novel
        # So he quickly decides to send a tip to him
        tx = await self.out(
            self.daemon.jsonrpc_claim_tip(claim3['claim_id'], '0.3', account_id=ramsey_account_id))
        await self.confirm_tx(tx['txid'])

        # And again checks if it went to the just right place
        resolve_result = await self.out(self.daemon.jsonrpc_resolve(uri))
        # Which it obviously did. Because....?????
        self.assertEqual(resolve_result[uri]['claim']['supports'][1]['amount'], '0.3')
        self.assertEqual(resolve_result[uri]['claim']['supports'][1]['txid'], tx['txid'])
        await self.generate(5)

        # Seeing the ravishing success of his novel Chris adds support to his claim too
        tx = await self.out(self.daemon.jsonrpc_claim_new_support('fresh-start', claim3['claim_id'], '0.4'))
        await self.confirm_tx(tx['txid'])

        # And check if his support showed up
        resolve_result = await self.out(self.daemon.jsonrpc_resolve(uri))
        # It did!
        self.assertEqual(resolve_result[uri]['claim']['supports'][2]['amount'], '0.4')
        self.assertEqual(resolve_result[uri]['claim']['supports'][2]['txid'], tx['txid'])
        await self.generate(5)

        # Now Ramsey who is a singer by profession, is preparing for his new "gig". He has everything in place for that
        # the instruments, the theatre, the ads, everything, EXCEPT lyrics!! He panicked.. But then he remembered
        # something, so he un-panicked. He quickly calls up his best bud Chris and requests him to write hit lyrics for
        # his song, seeing as his novel had smashed all the records, he was the perfect candidate!
        # .......
        # Chris agrees.. 17 hours 43 minutes and 14 seconds later, he makes his publish
        with tempfile.NamedTemporaryFile() as file:
            file.write(b'The Whale amd The Bookmark')
            file.write(b'I know right? Totally a hit song')
            file.write(b'That\'s what goes around for songs these days anyways')
            file.flush()
            claim4 = await self.out(self.daemon.jsonrpc_publish(
                'hit-song', '1.0', file_path=file.name, channel_id=channel['claim_id']
            ))
            self.assertTrue(claim4['success'])
            await self.confirm_tx(claim4['tx']['txid'])

        await self.generate(5)

        # He sends the link to Ramsey, all happy and proud
        uri = 'lbry://@spam/hit-song'

        # But sadly Ramsey wasn't so pleased. It was hard for him to tell Chris...
        # Chris, though a bit heartbroken, abandoned the claim for now, but instantly started working on new hit lyrics
        abandon = await self.out(self.daemon.jsonrpc_claim_abandon(txid=claim4['tx']['txid'], nout=0, blocking=False))
        self.assertTrue(abandon['success'])
        await self.confirm_tx(abandon['tx']['txid'])

        # He them checks that the claim doesn't resolve anymore.
        response = await self.out(self.daemon.jsonrpc_resolve(uri))
        self.assertNotIn('claim', response[uri])