# Introduction

This series of example playbooks show how to use Ansible to trigger Cloudformation.

It fufills the following behaviors, behavior driven development style:

## "As a user I should have a simple command that generates my `aws cloudformation` command for me"

Use `ansible-playbook` to run the appropriate command. The Ansible ties together the Cloudformation template, stack name, region so you have a single, short command to run.

## "As a user I want to easily migrate from the `aws cloudformation` command to this module (and back again, if required)"

I show how to use the [Cloudformation External Parameter JSON files](https://github.com/aws/aws-cli/issues/2275) to provide values to the Cloudformation template.

Ansible's built in Cloudformation support requires you to embed your parameter keys and values inside the Ansible task, which means these aren't portable to non Ansible / plain CLI usage.

However, the `cloudformation_with_params` uses a custom Ansible filter I wrote to properly translate `aws cloudformation` compatible external parameter files into what Ansible expects (in memory)

## "As a Cloudformation writer, sometimes I need to look up variables from deployed stacks"

The external parameter files make it relatively easy to provide static values into your cloudformation. However, sometimes you need to look up Cloudformation Outputs from previously deployed stacks (for example, VPC IDs).

I have an example to solve that problem too. `cloud9_with_lookup` embeds lookup commands into the mostly static external parameter file, using Ansible itself to execute the commands. The rendered file is then used by the cloudformation runner, in the same manner as the static parameters are.

# Additional Notes

## Testing Ansible setup on your system

    $ ansible-playbook playbooks/test.yml

Should return something, and look like it has worked. Won't actually install anything, because you better be running Python on your localhost, you're running Ansible...

## Using a non default AWS profile.

Use the `AWS_PROFILE` environmental variable, like so:

    $ AWS_PROFILE=profile_to_use_or_leave_out_for_default ansible-playbook playbooks/cloudformation_with_params_file.yml

## I want to see the dynamic lookup piece work

Order of commands to run

Must run:

    $ ansible-playbook playbooks/cloudformation_with_params_file.yml    

before:

    $ ansible-playbook playbooks/cloudformation_with_lookup.yml

(as the former generates an output the latter uses)

# "But why not X?"

I found I valued two things:

  1. Simplicity: ability to onboard new team members quickly. It's easier to explain 4 lines of connecting YAML than some custom Cloudformation System

  2. I want to be able to back away and use the aws cli if I want. (Granted, this stategy falls down with the dynamic lookup piece, but everything falls apart someday).

# "But why Ansible?"

I actually didn't start here! I started writing a Makfile (well, using Python's [Invoke](http://www.pyinvoke.org/) task runner).

But after about 2 cloudformation stack calls I wondered how many utility functions I would need to write to get things at a good, simple abstraction layer for my users. And that I'd need to bring in [cfn-create-or-update](https://cloudonaut.io/painlessly-create-or-update-cloudformation-stack-idempotent/), and that means I need to bring in some Node code in addition to my Python code.

Ansible does both of those things: having already written code that calls Cloudformation appropriately, and that handles created vs new resources.

And Ansible also essentially blocks until the Cloudformation task is done (and thrown an exit code if the Cloudformation didn't build properly). Super useful if you want to put this as part of a CI runner!

I have mostly had annoying experiences with Ansible in the past, but this kind of fit!
